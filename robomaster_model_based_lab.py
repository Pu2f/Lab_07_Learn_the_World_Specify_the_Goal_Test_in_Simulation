"""Week 07 lab: dynamics learning, reward shaping, and MPC with RoboMaster.

Only Python's standard library is used in mock mode. Physical mode additionally
requires DJI's RoboMaster Python SDK. Always validate in mock mode first.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import statistics
import sys
import threading
import time
from dataclasses import asdict, dataclass
from pathlib import Path


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def clip_vector(x: float, y: float, limit: float) -> tuple[float, float]:
    norm = math.hypot(x, y)
    scale = min(1.0, limit / norm) if norm else 1.0
    return x * scale, y * scale


def solve_linear_3(matrix: list[list[float]], vector: list[float]) -> list[float]:
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    for column in range(3):
        pivot = max(range(column, 3), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) < 1e-12:
            raise ValueError("calibration actions do not identify a full dynamics model")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        augmented[column] = [value / divisor for value in augmented[column]]
        for row in range(3):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [value - factor * pivot_value for value, pivot_value in zip(augmented[row], augmented[column])]
    return [augmented[row][3] for row in range(3)]


@dataclass
class DynamicsModel:
    dx_weights: list[float]
    dy_weights: list[float]
    dt: float
    source: str

    def predict(self, state: tuple[float, float], action: tuple[float, float]) -> tuple[float, float]:
        features = action[0] * self.dt, action[1] * self.dt, 1.0
        dx = sum(weight * feature for weight, feature in zip(self.dx_weights, features))
        dy = sum(weight * feature for weight, feature in zip(self.dy_weights, features))
        return state[0] + dx, state[1] + dy


def ideal_model(dt: float) -> DynamicsModel:
    return DynamicsModel([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], dt, "ideal")


def fit_dynamics(samples: list[dict], dt: float) -> tuple[DynamicsModel, float]:
    rows = [(sample["action_vx"] * dt, sample["action_vy"] * dt, 1.0) for sample in samples]
    matrix = [[sum(row[i] * row[j] for row in rows) for j in range(3)] for i in range(3)]
    for index in range(3):
        matrix[index][index] += 1e-8

    def fit(key: str) -> list[float]:
        vector = [sum(row[i] * sample[key] for row, sample in zip(rows, samples)) for i in range(3)]
        return solve_linear_3(matrix, vector)

    model = DynamicsModel(fit("delta_x"), fit("delta_y"), dt, "learned")
    errors = []
    for sample in samples:
        predicted = model.predict((0.0, 0.0), (sample["action_vx"], sample["action_vy"]))
        errors.append((predicted[0] - sample["delta_x"]) ** 2 + (predicted[1] - sample["delta_y"]) ** 2)
    return model, math.sqrt(statistics.fmean(errors))


class MockController:
    """A small simulator with cross-axis coupling and observation noise."""

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        self.x = self.y = 0.0

    def begin_trial(self) -> None:
        self.x = self.y = 0.0

    def position(self) -> tuple[float, float]:
        return self.x, self.y

    def command(self, vx: float, vy: float, duration: float) -> None:
        self.x += (0.86 * vx + 0.07 * vy) * duration + 0.001 + self.rng.gauss(0, 0.002)
        self.y += (-0.04 * vx + 0.92 * vy) * duration - 0.001 + self.rng.gauss(0, 0.002)

    def stop(self) -> None:
        pass

    def close(self) -> None:
        pass


class RoboMasterController:
    """Minimal adapter around drive_speed and chassis position subscription."""

    def __init__(self, conn_type: str, frequency: int) -> None:
        try:
            from robomaster import robot
        except ImportError as error:
            raise SystemExit("ไม่พบ RoboMaster SDK: ติดตั้งด้วย 'python -m pip install robomaster'") from error

        self._position = (0.0, 0.0)
        self._origin = (0.0, 0.0)
        self._ready = threading.Event()
        self.robot = robot.Robot()
        self.robot.initialize(conn_type=conn_type)
        self.chassis = self.robot.chassis
        if not self.chassis.sub_position(cs=1, freq=frequency, callback=self._position_callback):
            self.robot.close()
            raise SystemExit("สมัครรับข้อมูลตำแหน่ง chassis ไม่สำเร็จ")
        if not self._ready.wait(4):
            self.close()
            raise SystemExit("ไม่ได้รับข้อมูลตำแหน่งจาก chassis ภายใน 4 วินาที")

    def _position_callback(self, data) -> None:
        self._position = float(data[0]), float(data[1])
        self._ready.set()

    def begin_trial(self) -> None:
        self._origin = self._position

    def position(self) -> tuple[float, float]:
        return self._position[0] - self._origin[0], self._position[1] - self._origin[1]

    def command(self, vx: float, vy: float, duration: float) -> None:
        self.chassis.drive_speed(x=vx, y=vy, z=0, timeout=max(0.5, duration * 2))
        time.sleep(duration)
        self.stop()
        time.sleep(0.08)

    def stop(self) -> None:
        self.chassis.drive_speed(x=0, y=0, z=0, timeout=1)

    def close(self) -> None:
        try:
            self.stop()
            self.chassis.unsub_position()
        finally:
            self.robot.close()


def calibration_actions(speed: float, repeats: int) -> list[tuple[float, float]]:
    diagonal = speed / math.sqrt(2)
    block = [
        (speed, 0.0), (-speed, 0.0), (0.0, speed), (0.0, -speed),
        (diagonal, diagonal), (-diagonal, -diagonal),
        (diagonal, -diagonal), (-diagonal, diagonal),
    ]
    return block * repeats


def collect_calibration(controller, args: argparse.Namespace) -> tuple[list[dict], DynamicsModel, float]:
    if args.mode == "robot":
        input("วางหุ่นที่ S หันหัวตามแกน +x ตรวจพื้นที่ว่าง แล้วกด Enter เพื่อเก็บ calibration...")
    controller.begin_trial()
    records = []
    for index, action in enumerate(calibration_actions(args.calibration_speed, args.calibration_repeats), 1):
        before = controller.position()
        controller.command(*action, args.dt)
        after = controller.position()
        record = {
            "sample": index,
            "action_vx": action[0],
            "action_vy": action[1],
            "before_x": before[0],
            "before_y": before[1],
            "after_x": after[0],
            "after_y": after[1],
            "delta_x": after[0] - before[0],
            "delta_y": after[1] - before[1],
        }
        records.append(record)
        print(f"sample={index:02d} action=({action[0]:+.2f},{action[1]:+.2f}) delta=({record['delta_x']:+.3f},{record['delta_y']:+.3f})")
    controller.stop()
    model, rmse = fit_dynamics(records, args.dt)
    return records, model, rmse


def save_calibration(output_dir: Path, records: list[dict], model: DynamicsModel, rmse: float) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "calibration.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=records[0])
        writer.writeheader()
        writer.writerows(records)
    (output_dir / "model.json").write_text(json.dumps({
        "source": model.source,
        "dt": model.dt,
        "dx_weights": model.dx_weights,
        "dy_weights": model.dy_weights,
        "fit_rmse_m": rmse,
        "equation": "delta = W @ [vx*dt, vy*dt, 1]",
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def load_model(path: Path, dt: float) -> DynamicsModel:
    data = json.loads(path.read_text(encoding="utf-8"))
    if abs(float(data["dt"]) - dt) > 1e-9:
        raise SystemExit(f"model ใช้ dt={data['dt']} แต่คำสั่ง plan ใช้ dt={dt}; ให้ใช้ค่าเดียวกับ calibration")
    return DynamicsModel(list(map(float, data["dx_weights"])), list(map(float, data["dy_weights"])), dt, "learned")


def transition_reward(before: tuple[float, float], after: tuple[float, float], args: argparse.Namespace) -> tuple[float, bool]:
    before_distance = math.hypot(args.target_x - before[0], args.target_y - before[1])
    after_distance = math.hypot(args.target_x - after[0], args.target_y - after[1])
    terminal = after_distance <= args.goal_tolerance
    base_reward = 1.0 if terminal else 0.0
    if args.reward == "sparse":
        return base_reward, terminal
    potential_before, potential_after = -before_distance, -after_distance
    return base_reward + args.gamma * potential_after - potential_before, terminal


def sequence_score(model: DynamicsModel, start: tuple[float, float], sequence: list[tuple[float, float]], args: argparse.Namespace) -> float:
    state, total, discount = start, 0.0, 1.0
    for action in sequence:
        successor = model.predict(state, action)
        reward, terminal = transition_reward(state, successor, args)
        total += discount * reward
        state, discount = successor, discount * args.gamma
        if terminal:
            break
    return total


def plan_action(model: DynamicsModel, state: tuple[float, float], args: argparse.Namespace, rng: random.Random) -> tuple[tuple[float, float], float]:
    dimensions = args.horizon * 2
    means = [0.0] * dimensions
    deviations = [args.max_speed * 0.75] * dimensions
    best_score = float("-inf")
    for _ in range(args.iterations):
        samples = []
        for _ in range(args.samples):
            flat = [rng.gauss(mean, deviation) for mean, deviation in zip(means, deviations)]
            sequence = [clip_vector(flat[index], flat[index + 1], args.max_speed) for index in range(0, dimensions, 2)]
            score = sequence_score(model, state, sequence, args)
            samples.append((score, sequence))
            best_score = max(best_score, score)

        if args.planner == "cem":
            elite_count = min(args.samples, max(2, round(args.samples * args.elite_fraction)))
            selected = sorted(samples, key=lambda item: item[0], reverse=True)[:elite_count]
            weights = [1 / elite_count] * elite_count
        else:
            maximum = max(score for score, _ in samples)
            raw_weights = [math.exp((score - maximum) / args.temperature) for score, _ in samples]
            total_weight = sum(raw_weights)
            selected, weights = samples, [weight / total_weight for weight in raw_weights]

        flattened = [[component for action in sequence for component in action] for _, sequence in selected]
        means = [sum(weight * values[index] for weight, values in zip(weights, flattened)) for index in range(dimensions)]
        deviations = [
            max(0.015, math.sqrt(sum(weight * (values[index] - means[index]) ** 2 for weight, values in zip(weights, flattened))))
            for index in range(dimensions)
        ]
    return clip_vector(means[0], means[1], args.max_speed), best_score


@dataclass
class RolloutRecord:
    step: int
    x: float
    y: float
    distance_before: float
    action_vx: float
    action_vy: float
    planner_score: float
    predicted_next_x: float
    predicted_next_y: float
    actual_next_x: float
    actual_next_y: float
    one_step_model_error_m: float
    distance_after: float
    reward: float
    terminal: bool


def run_plan(controller, model: DynamicsModel, args: argparse.Namespace, rng: random.Random) -> tuple[list[RolloutRecord], dict]:
    if args.mode == "robot":
        input("วางหุ่นที่ S หันหัวตามแกน +x และตรวจว่าไม่มีคนในสนาม แล้วกด Enter เพื่อเริ่ม MPC...")
    controller.begin_trial()
    records = []
    path_length = total_reward = 0.0
    for step in range(1, args.max_steps + 1):
        state = controller.position()
        distance_before = math.hypot(args.target_x - state[0], args.target_y - state[1])
        if distance_before <= args.goal_tolerance:
            break
        if math.hypot(*state) > args.arena_limit:
            print("หยุด: หุ่นออกนอกขอบเขตที่กำหนด")
            break
        action, planner_score = plan_action(model, state, args, rng)
        predicted = model.predict(state, action)
        controller.command(*action, args.dt)
        actual = controller.position()
        path_length += math.hypot(actual[0] - state[0], actual[1] - state[1])
        reward, terminal = transition_reward(state, actual, args)
        total_reward += reward
        distance_after = math.hypot(args.target_x - actual[0], args.target_y - actual[1])
        model_error = math.hypot(predicted[0] - actual[0], predicted[1] - actual[1])
        records.append(RolloutRecord(
            step, state[0], state[1], distance_before, action[0], action[1], planner_score,
            predicted[0], predicted[1], actual[0], actual[1], model_error,
            distance_after, reward, terminal,
        ))
        print(f"step={step:02d} action=({action[0]:+.2f},{action[1]:+.2f}) distance={distance_after:.3f}m model_error={model_error:.3f}m")
        if terminal:
            break
    controller.stop()
    final_state = controller.position()
    final_distance = math.hypot(args.target_x - final_state[0], args.target_y - final_state[1])
    summary = {
        "mode": args.mode,
        "model_source": model.source,
        "planner": args.planner,
        "reward": args.reward,
        "success": final_distance <= args.goal_tolerance,
        "steps": len(records),
        "return": total_reward,
        "final_x": final_state[0],
        "final_y": final_state[1],
        "final_distance_m": final_distance,
        "path_length_m": path_length,
        "mean_one_step_model_error_m": statistics.fmean(record.one_step_model_error_m for record in records) if records else 0.0,
        "max_one_step_model_error_m": max((record.one_step_model_error_m for record in records), default=0.0),
    }
    return records, summary


def save_rollout(output_dir: Path, records: list[RolloutRecord], summary: dict, args: argparse.Namespace) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "rollout.csv").open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=RolloutRecord.__dataclass_fields__)
        writer.writeheader()
        writer.writerows(asdict(record) for record in records)
    parameters = vars(args).copy()
    parameters["output_dir"] = str(args.output_dir)
    parameters["model_file"] = str(args.model_file) if args.model_file else None
    (output_dir / "summary.json").write_text(
        json.dumps({"summary": summary, "parameters": parameters}, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def motion_check(controller, args: argparse.Namespace) -> None:
    if args.mode == "robot":
        input("ตรวจพื้นที่ว่างอย่างน้อย 2×2 เมตร แล้วกด Enter เพื่อวิ่งสี่เหลี่ยม 0.20 m...")
    controller.begin_trial()
    for label, vx, vy in (("+x", 0.20, 0), ("+y", 0, 0.20), ("-x", -0.20, 0), ("-y", 0, -0.20)):
        print("motion check", label)
        controller.command(vx, vy, 1.0)
    print("ตำแหน่งหลัง motion check:", tuple(round(value, 3) for value in controller.position()))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Week 07: model-based control with DJI RoboMaster")
    parser.add_argument("--phase", choices=("collect", "plan"), default="collect")
    parser.add_argument("--mode", choices=("mock", "robot"), default="mock")
    parser.add_argument("--conn-type", choices=("ap", "sta", "rndis"), default="ap")
    parser.add_argument("--model-source", choices=("learned", "ideal"), default="learned")
    parser.add_argument("--model-file", type=Path)
    parser.add_argument("--planner", choices=("cem", "mppi"), default="cem")
    parser.add_argument("--reward", choices=("sparse", "potential"), default="potential")
    parser.add_argument("--target-x", type=float, default=0.70)
    parser.add_argument("--target-y", type=float, default=0.35)
    parser.add_argument("--goal-tolerance", type=float, default=0.10)
    parser.add_argument("--max-speed", type=float, default=0.25)
    parser.add_argument("--dt", type=float, default=0.40)
    parser.add_argument("--max-steps", type=int, default=24)
    parser.add_argument("--horizon", type=int, default=6)
    parser.add_argument("--samples", type=int, default=160)
    parser.add_argument("--iterations", type=int, default=4)
    parser.add_argument("--elite-fraction", type=float, default=0.15)
    parser.add_argument("--temperature", type=float, default=0.10)
    parser.add_argument("--gamma", type=float, default=0.95)
    parser.add_argument("--calibration-speed", type=float, default=0.20)
    parser.add_argument("--calibration-repeats", type=int, default=3)
    parser.add_argument("--arena-limit", type=float, default=1.20)
    parser.add_argument("--position-frequency", type=int, choices=(1, 5, 10, 20, 50), default=20)
    parser.add_argument("--motion-check", action="store_true")
    parser.add_argument("--arm-robot", action="store_true")
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--output-dir", type=Path, default=Path("lab-output"))
    args = parser.parse_args()
    positive = (args.goal_tolerance, args.max_speed, args.dt, args.temperature, args.calibration_speed, args.arena_limit)
    if min(positive) <= 0 or min(args.max_steps, args.horizon, args.iterations, args.calibration_repeats) < 1 or args.samples < 2:
        parser.error("ค่าระยะ เวลา ความเร็ว และจำนวนรอบต้องเป็นค่าบวก")
    if not 0 < args.elite_fraction <= 1 or not 0 <= args.gamma <= 1:
        parser.error("ต้องมี 0<elite-fraction≤1 และ 0≤gamma≤1")
    if math.hypot(args.target_x, args.target_y) >= args.arena_limit:
        parser.error("target ต้องอยู่ภายใน --arena-limit")
    if args.phase == "plan" and args.model_source == "learned" and not args.model_file:
        parser.error("plan ด้วย learned model ต้องระบุ --model-file")
    if args.phase == "plan" and args.model_source == "learned" and not args.model_file.is_file():
        parser.error(f"ไม่พบ model file: {args.model_file}")
    if args.mode == "robot" and not args.arm_robot:
        parser.error("โหมด robot ต้องยืนยันด้วย --arm-robot หลังตรวจ safety checklist")
    if args.mode == "robot" and (args.max_speed > 0.30 or args.calibration_speed > 0.20 or args.dt > 0.50):
        parser.error("physical lab จำกัด max-speed≤0.30, calibration-speed≤0.20 m/s และ dt≤0.50 s")
    if args.mode == "robot" and args.phase == "plan" and args.reward == "sparse":
        parser.error("sparse reward ใช้เปรียบเทียบใน mock mode เท่านั้น; robot ต้องใช้ --reward potential")
    return args


def main() -> None:
    args = parse_args()
    rng = random.Random(args.seed)
    controller = MockController(rng) if args.mode == "mock" else RoboMasterController(args.conn_type, args.position_frequency)
    try:
        if args.motion_check:
            motion_check(controller, args)
        elif args.phase == "collect":
            records, model, rmse = collect_calibration(controller, args)
            save_calibration(args.output_dir, records, model, rmse)
            print("learned dx weights:", [round(value, 4) for value in model.dx_weights])
            print("learned dy weights:", [round(value, 4) for value in model.dy_weights])
            print(f"fit RMSE={rmse:.4f} m")
            print("บันทึก model ที่", (args.output_dir / "model.json").resolve())
        else:
            model = ideal_model(args.dt) if args.model_source == "ideal" else load_model(args.model_file, args.dt)
            records, summary = run_plan(controller, model, args, rng)
            save_rollout(args.output_dir, records, summary, args)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            print("บันทึกผลที่", args.output_dir.resolve())
    except KeyboardInterrupt:
        print("\nหยุดโดยผู้ใช้")
    finally:
        controller.close()


if __name__ == "__main__":
    main()
