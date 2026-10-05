# Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation

เอกสารนี้รวบรวมผลการทดลองจาก Terminal โดยจัดกลุ่มตามขั้นตอนการทำงานเดิม และคงรายละเอียดผลลัพธ์ไว้ครบถ้วน

## 1. Motion Check — Mock Mode

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --mode mock --motion-check
motion check +x
motion check +y
motion check -x
motion check -y
ตำแหน่งหลัง motion check: (0.002, -0.009)
```

## 2. Motion Check — Robot Mode

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --mode robot --motion-check --arm-robot
ตรวจพื้นที่ว่างอย่างน้อย 2×2 เมตร แล้วกด Enter เพื่อวิ่งสี่เหลี่ยม 0.20 m...
motion check +x
motion check +y
motion check -x
motion check -y
ตำแหน่งหลัง motion check: (0.008, -0.003)
```

## 3. Collect Calibration — Mock Mode

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase collect --mode mock --output-di[...]
sample=01 action=(+0.20,+0.00) delta=(+0.066,-0.005)
sample=02 action=(-0.20,+0.00) delta=(-0.066,+0.002)
sample=03 action=(+0.00,+0.20) delta=(+0.007,+0.069)
sample=04 action=(+0.00,-0.20) delta=(-0.005,-0.075)
sample=05 action=(+0.14,+0.14) delta=(+0.056,+0.049)
sample=06 action=(-0.14,-0.14) delta=(-0.052,-0.052)
sample=07 action=(+0.14,-0.14) delta=(+0.044,-0.055)
sample=08 action=(-0.14,+0.14) delta=(-0.041,+0.049)
sample=09 action=(+0.20,+0.00) delta=(+0.064,-0.000)
sample=10 action=(-0.20,+0.00) delta=(-0.064,+0.004)
sample=11 action=(+0.00,+0.20) delta=(+0.007,+0.072)
sample=12 action=(+0.00,-0.20) delta=(-0.005,-0.077)
sample=13 action=(+0.14,+0.14) delta=(+0.055,+0.048)
sample=14 action=(-0.14,-0.14) delta=(-0.056,-0.052)
sample=15 action=(+0.14,-0.14) delta=(+0.045,-0.057)
sample=16 action=(-0.14,+0.14) delta=(-0.040,+0.056)
sample=17 action=(+0.20,+0.00) delta=(+0.063,-0.003)
sample=18 action=(-0.20,+0.00) delta=(-0.065,+0.005)
sample=19 action=(+0.00,+0.20) delta=(+0.008,+0.068)
sample=20 action=(+0.00,-0.20) delta=(-0.003,-0.074)
sample=21 action=(+0.14,+0.14) delta=(+0.057,+0.050)
sample=22 action=(-0.14,-0.14) delta=(-0.055,-0.047)
sample=23 action=(+0.14,-0.14) delta=(+0.043,-0.053)
sample=24 action=(-0.14,+0.14) delta=(-0.043,+0.052)
learned dx weights: [0.836, 0.0919, 0.0009]
learned dy weights: [-0.0365, 0.9117, -0.0011]
fit RMSE=0.0030 m
บันทึก model ที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/mock-model/model.json
```

## 4. Collect Calibration — Robot Mode

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase collect --mode robot --arm-robo[...]
วางหุ่นที่ S หันหัวตามแกน +x ตรวจพื้นที่ว่าง แล้วกด Enter เพื่อเก็บ calibration...
sample=01 action=(+0.20,+0.00) delta=(+0.001,-0.079)
sample=02 action=(-0.20,+0.00) delta=(-0.001,+0.075)
sample=03 action=(+0.00,+0.20) delta=(+0.077,-0.003)
sample=04 action=(+0.00,-0.20) delta=(-0.075,-0.000)
sample=05 action=(+0.14,+0.14) delta=(+0.037,-0.075)
sample=06 action=(-0.14,-0.14) delta=(-0.046,+0.058)
sample=07 action=(+0.14,-0.14) delta=(-0.065,-0.052)
sample=08 action=(-0.14,+0.14) delta=(+0.054,+0.060)
sample=09 action=(+0.20,+0.00) delta=(+0.000,-0.084)
sample=10 action=(-0.20,+0.00) delta=(+0.001,+0.091)
sample=11 action=(+0.00,+0.20) delta=(+0.074,-0.004)
sample=12 action=(+0.00,-0.20) delta=(-0.062,+0.005)
sample=13 action=(+0.14,+0.14) delta=(+0.013,-0.072)
sample=14 action=(-0.14,-0.14) delta=(-0.040,+0.052)
sample=15 action=(+0.14,-0.14) delta=(-0.066,-0.042)
sample=16 action=(-0.14,+0.14) delta=(+0.060,+0.062)
sample=17 action=(+0.20,+0.00) delta=(-0.004,-0.085)
sample=18 action=(-0.20,+0.00) delta=(+0.001,+0.085)
sample=19 action=(+0.00,+0.20) delta=(+0.071,-0.004)
sample=20 action=(+0.00,-0.20) delta=(-0.069,+0.006)
sample=21 action=(+0.14,+0.14) delta=(+0.023,-0.071)
sample=22 action=(-0.14,-0.14) delta=(-0.037,+0.049)
sample=23 action=(+0.14,-0.14) delta=(-0.073,-0.049)
sample=24 action=(-0.14,+0.14) delta=(+0.065,+0.060)
learned dx weights: [-0.1419, 0.8734, -0.0025]
learned dy weights: [-1.0361, -0.0611, -0.0007]
fit RMSE=0.0121 m
บันทึก model ที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/robot-model/model.json

(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ code .
```

## 5. Plan — Mock Mode — Sparse Reward with CEM

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase plan --mode mock --model-file r[...]
step=01 action=(-0.03,+0.01) distance=0.794m model_error=0.005m
step=02 action=(-0.02,-0.02) distance=0.808m model_error=0.005m
step=03 action=(+0.02,-0.02) distance=0.806m model_error=0.002m
step=04 action=(-0.03,+0.00) distance=0.814m model_error=0.002m
step=05 action=(-0.03,+0.00) distance=0.822m model_error=0.001m
step=06 action=(+0.00,+0.03) distance=0.815m model_error=0.002m
step=07 action=(-0.03,+0.07) distance=0.812m model_error=0.001m
step=08 action=(+0.00,-0.05) distance=0.818m model_error=0.002m
step=09 action=(-0.05,-0.07) distance=0.853m model_error=0.006m
step=10 action=(+0.02,+0.07) distance=0.832m model_error=0.002m
step=11 action=(-0.00,+0.02) distance=0.831m model_error=0.002m
step=12 action=(+0.04,+0.03) distance=0.814m model_error=0.002m
step=13 action=(-0.01,+0.02) distance=0.815m model_error=0.001m
step=14 action=(+0.07,+0.04) distance=0.787m model_error=0.002m
step=15 action=(-0.02,-0.05) distance=0.801m model_error=0.002m
step=16 action=(+0.04,-0.07) distance=0.801m model_error=0.003m
step=17 action=(-0.05,-0.02) distance=0.819m model_error=0.001m
step=18 action=(+0.07,+0.03) distance=0.790m model_error=0.002m
step=19 action=(+0.02,-0.05) distance=0.793m model_error=0.002m
step=20 action=(+0.00,-0.05) distance=0.802m model_error=0.000m
step=21 action=(+0.00,-0.06) distance=0.813m model_error=0.002m
step=22 action=(+0.00,-0.00) distance=0.811m model_error=0.004m
step=23 action=(-0.04,+0.01) distance=0.817m model_error=0.000m
step=24 action=(+0.05,+0.03) distance=0.797m model_error=0.001m
{
  "mode": "mock",
  "model_source": "learned",
  "planner": "cem",
  "reward": "sparse",
  "success": false,
  "steps": 24,
  "return": 0.0,
  "final_x": 0.01801615436032923,
  "final_y": -0.06211425414432729,
  "final_distance_m": 0.7968313022104551,
  "path_length_m": 0.4228016579003992,
  "mean_one_step_model_error_m": 0.0023191218527873394,
  "max_one_step_model_error_m": 0.005972213755140512
}
บันทึกผลที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/mock-sparse
```

## 6. Plan — Mock Mode — Potential Reward with CEM

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase plan --mode mock --model-file [...]
step=01 action=(+0.17,+0.12) distance=0.712m model_error=0.004m
step=02 action=(+0.19,+0.09) distance=0.641m model_error=0.004m
step=03 action=(+0.19,+0.09) distance=0.566m model_error=0.003m
step=04 action=(+0.16,+0.12) distance=0.494m model_error=0.002m
step=05 action=(+0.21,+0.10) distance=0.413m model_error=0.001m
step=06 action=(+0.19,+0.11) distance=0.334m model_error=0.003m
step=07 action=(+0.19,+0.12) distance=0.256m model_error=0.002m
step=08 action=(+0.19,+0.12) distance=0.176m model_error=0.002m
step=09 action=(+0.22,+0.11) distance=0.094m model_error=0.005m
{
  "mode": "mock",
  "model_source": "learned",
  "planner": "cem",
  "reward": "potential",
  "success": true,
  "steps": 9,
  "return": 1.872575916182533,
  "final_x": 0.6115815908193928,
  "final_y": 0.317023646311975,
  "final_distance_m": 0.09436765857319443,
  "path_length_m": 0.6901061697089184,
  "mean_one_step_model_error_m": 0.002922810420361314,
  "max_one_step_model_error_m": 0.00490835881345853
}
บันทึกผลที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/mock-shaped
```

## 7. Repeated Plan Commands — Mock Mode

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase plan --mode mock --model-file [...]

python robomaster_model_based_lab.py --phase plan --mode mock --model-file results/mock-model/model.json --reward potential --planner cem --output-dir results/mock-shaped
step=01 action=(-0.03,+0.01) distance=0.794m model_error=0.005m
step=02 action=(-0.02,-0.02) distance=0.808m model_error=0.005m
step=03 action=(+0.02,-0.02) distance=0.806m model_error=0.002m
step=04 action=(-0.03,+0.00) distance=0.814m model_error=0.002m
step=05 action=(-0.03,+0.00) distance=0.822m model_error=0.001m
step=06 action=(+0.00,+0.03) distance=0.815m model_error=0.002m
step=07 action=(-0.03,+0.07) distance=0.812m model_error=0.001m
step=08 action=(+0.00,-0.05) distance=0.818m model_error=0.002m
step=09 action=(-0.05,-0.07) distance=0.853m model_error=0.006m
step=10 action=(+0.02,+0.07) distance=0.832m model_error=0.002m
step=11 action=(-0.00,+0.02) distance=0.831m model_error=0.002m
step=12 action=(+0.04,+0.03) distance=0.814m model_error=0.002m
step=13 action=(-0.01,+0.02) distance=0.815m model_error=0.001m
step=14 action=(+0.07,+0.04) distance=0.787m model_error=0.002m
step=15 action=(-0.02,-0.05) distance=0.801m model_error=0.002m
step=16 action=(+0.04,-0.07) distance=0.801m model_error=0.003m
step=17 action=(-0.05,-0.02) distance=0.819m model_error=0.001m
step=18 action=(+0.07,+0.03) distance=0.790m model_error=0.002m
step=19 action=(+0.02,-0.05) distance=0.793m model_error=0.002m
step=20 action=(+0.00,-0.05) distance=0.802m model_error=0.000m
step=21 action=(+0.00,-0.06) distance=0.813m model_error=0.002m
step=22 action=(+0.00,-0.00) distance=0.811m model_error=0.004m
step=23 action=(-0.04,+0.01) distance=0.817m model_error=0.000m
step=24 action=(+0.05,+0.03) distance=0.797m model_error=0.001m
{
  "mode": "mock",
  "model_source": "learned",
  "planner": "cem",
  "reward": "sparse",
  "success": false,
  "steps": 24,
  "return": 0.0,
  "final_x": 0.01801615436032923,
  "final_y": -0.06211425414432729,
  "final_distance_m": 0.7968313022104551,
  "path_length_m": 0.4228016579003992,
  "mean_one_step_model_error_m": 0.0023191218527873394,
  "max_one_step_model_error_m": 0.005972213755140512
}
บันทึกผลที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/mock-sparse
step=01 action=(+0.17,+0.12) distance=0.712m model_error=0.004m
step=02 action=(+0.19,+0.09) distance=0.641m model_error=0.004m
step=03 action=(+0.19,+0.09) distance=0.566m model_error=0.003m
step=04 action=(+0.16,+0.12) distance=0.494m model_error=0.002m
step=05 action=(+0.21,+0.10) distance=0.413m model_error=0.001m
step=06 action=(+0.19,+0.11) distance=0.334m model_error=0.003m
step=07 action=(+0.19,+0.12) distance=0.256m model_error=0.002m
step=08 action=(+0.19,+0.12) distance=0.176m model_error=0.002m
step=09 action=(+0.22,+0.11) distance=0.094m model_error=0.005m
{
  "mode": "mock",
  "model_source": "learned",
  "planner": "cem",
  "reward": "potential",
  "success": true,
  "steps": 9,
  "return": 1.872575916182533,
  "final_x": 0.6115815908193928,
  "final_y": 0.317023646311975,
  "final_distance_m": 0.09436765857319443,
  "path_length_m": 0.6901061697089184,
  "mean_one_step_model_error_m": 0.002922810420361314,
  "max_one_step_model_error_m": 0.00490835881345853
}
บันทึกผลที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/mock-shaped
```

## 8. Plan — Mock Mode — Potential Reward with MPPI

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase plan --mode mock --model-file [...]
step=01 action=(+0.11,+0.08) distance=0.738m model_error=0.005m
step=02 action=(+0.11,+0.03) distance=0.702m model_error=0.004m
step=03 action=(+0.11,+0.05) distance=0.657m model_error=0.003m
step=04 action=(+0.09,+0.06) distance=0.617m model_error=0.002m
step=05 action=(+0.13,+0.07) distance=0.567m model_error=0.001m
step=06 action=(+0.12,+0.07) distance=0.516m model_error=0.002m
step=07 action=(+0.10,+0.06) distance=0.474m model_error=0.001m
step=08 action=(+0.18,+0.02) distance=0.414m model_error=0.003m
step=09 action=(+0.12,+0.10) distance=0.365m model_error=0.006m
step=10 action=(+0.06,+0.19) distance=0.308m model_error=0.001m
step=11 action=(+0.19,+0.06) distance=0.239m model_error=0.003m
step=12 action=(+0.17,+0.08) distance=0.173m model_error=0.002m
step=13 action=(+0.18,+0.10) distance=0.102m model_error=0.001m
step=14 action=(+0.16,+0.08) distance=0.038m model_error=0.002m
{
  "mode": "mock",
  "model_source": "learned",
  "planner": "mppi",
  "reward": "potential",
  "success": true,
  "steps": 14,
  "return": 2.0400335920279185,
  "final_x": 0.6651833412191765,
  "final_y": 0.3343816261587843,
  "final_distance_m": 0.03815931511576508,
  "path_length_m": 0.7705720865643543,
  "mean_one_step_model_error_m": 0.0026340702657088543,
  "max_one_step_model_error_m": 0.005765271689709258
}
บันทึกผลที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/mock-mppi
```

## 9. Plan — Robot Mode — Connection Error

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase plan --mode robot --conn-type [...]
Traceback (most recent call last):
  File "robomaster_model_based_lab.py", line 446, in <module>
    main()
  File "robomaster_model_based_lab.py", line 422, in main
    controller = MockController(rng) if args.mode == "mock" else RoboMasterController(args.conn_type, args.position_frequency)
  File "robomaster_model_based_lab.py", line 122, in __init__
    self.robot.initialize(conn_type=conn_type)
  File "/home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/.venv/lib/python3.8/site-packages/robomaster/robot.py", line 1300, in initialize
    conn1 = self._wait_for_connection(conn_type, proto_type, sn)
  File "/home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/.venv/lib/python3.8/site-packages/robomaster/robot.py", line 1351, in _wait_for_connection
    result, local_addr, remote_addr = self._sdk_conn.request_connection(self._sdk_host, conn_type, proto_type, sn)
  File "/home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/.venv/lib/python3.8/site-packages/robomaster/conn.py", line 322, in request_connection
    "proxy addr {2}".format(local_addr, remote_addr, proxy_addr))
UnboundLocalError: local variable 'proxy_addr' referenced before assignment
```

## 10. Plan — Robot Mode — Learned Model with CEM

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase plan --mode robot --arm-robot [...]
วางหุ่นที่ S หันหัวตามแกน +x และตรวจว่าไม่มีคนในสนาม แล้วกด Enter เพื่อเริ่[...]
step=01 action=(-0.11,+0.19) distance=0.691m model_error=0.022m
step=02 action=(-0.10,+0.19) distance=0.614m model_error=0.018m
step=03 action=(-0.09,+0.18) distance=0.532m model_error=0.020m
step=04 action=(-0.07,+0.18) distance=0.459m model_error=0.005m
step=05 action=(-0.08,+0.18) distance=0.372m model_error=0.019m
step=06 action=(-0.08,+0.18) distance=0.286m model_error=0.020m
step=07 action=(-0.07,+0.21) distance=0.193m model_error=0.019m
step=08 action=(-0.10,+0.22) distance=0.091m model_error=0.023m
{
  "mode": "robot",
  "model_source": "learned",
  "planner": "cem",
  "reward": "potential",
  "success": true,
  "steps": 8,
  "return": 1.8533029961848153,
  "final_x": 0.63321,
  "final_y": 0.28781999999999996,
  "final_distance_m": 0.09125380266049185,
  "path_length_m": 0.7106429901680617,
  "mean_one_step_model_error_m": 0.018330392411023355,
  "max_one_step_model_error_m": 0.023170719851705317
}
บันทึกผลที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/robot-learned
```

## 11. Plan — Robot Mode — Ideal Model with CEM

```text
(.venv) pcn@pcn-ThinkPad-E14-Gen-8:~/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation$ python robomaster_model_based_lab.py --phase plan --mode robot --arm-robot [...]
วางหุ่นที่ S หันหัวตามแกน +x และตรวจว่าไม่มีคนในสนาม แล้วกด Enter เพื่อเริ่[...]
step=01 action=(+0.18,+0.09) distance=0.860m model_error=0.159m
step=02 action=(+0.18,+0.12) distance=0.948m model_error=0.176m
step=03 action=(+0.19,+0.08) distance=1.045m model_error=0.180m
step=04 action=(+0.14,+0.13) distance=1.133m model_error=0.164m
step=05 action=(+0.17,+0.12) distance=1.218m model_error=0.168m
step=06 action=(+0.19,+0.09) distance=1.320m model_error=0.185m
step=07 action=(+0.19,+0.11) distance=1.407m model_error=0.173m
step=08 action=(+0.20,+0.10) distance=1.508m model_error=0.189m
step=09 action=(+0.17,+0.09) distance=1.593m model_error=0.164m
step=10 action=(+0.19,+0.09) distance=1.690m model_error=0.180m
step=11 action=(+0.17,+0.14) distance=1.791m model_error=0.187m
step=12 action=(+0.16,+0.14) distance=1.878m model_error=0.170m
step=13 action=(+0.19,+0.08) distance=1.974m model_error=0.177m
step=14 action=(+0.20,+0.09) distance=2.072m model_error=0.185m
หยุด: หุ่นออกนอกขอบเขตที่กำหนด
{
  "mode": "robot",
  "model_source": "ideal",
  "planner": "cem",
  "reward": "potential",
  "success": false,
  "steps": 14,
  "return": -0.2671923383380773,
  "final_x": -1.1826699999999999,
  "final_y": -0.51467,
  "final_distance_m": 2.071738530268721,
  "path_length_m": 1.2923704104747515,
  "mean_one_step_model_error_m": 0.17540625297480256,
  "max_one_step_model_error_m": 0.18878321282982372
}
บันทึกผลที่ /home/pcn/Classworks/Assignments/Lab_07_Learn_the_World_Specify_the_Goal_Test_in_Simulation/results/robot-ideal
```
