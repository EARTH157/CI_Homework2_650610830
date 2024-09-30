import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# 1. กำหนดตัวแปรฟัซซี่
current_floor = ctrl.Antecedent(np.arange(0, 11, 1), 'current_floor')  # 0 ถึง 10 ชั้น
request_floor = ctrl.Antecedent(np.arange(0, 11, 1), 'request_floor')
direction = ctrl.Antecedent(np.array([0, 1]), 'direction')  # 0 = หยุด, 1 = เคลื่อนที่
movement = ctrl.Consequent(np.arange(-1, 2, 1), 'movement')  # -1 = ลง, 0 = หยุด, 1 = ขึ้น

# 2. กำหนด membership functions
direction['stop'] = fuzz.trimf(direction.universe, [0, 0, 0])
direction['move'] = fuzz.trimf(direction.universe, [1, 1, 1])

movement['down'] = fuzz.trimf(movement.universe, [-1, -1, -1])
movement['stop'] = fuzz.trimf(movement.universe, [0, 0, 0])
movement['up'] = fuzz.trimf(movement.universe, [1, 1, 1])

current_floor['low'] = fuzz.trimf(current_floor.universe, [0, 0, 5])
current_floor['medium'] = fuzz.trimf(current_floor.universe, [2, 5, 8])
current_floor['high'] = fuzz.trimf(current_floor.universe, [5, 10, 10])

request_floor['low'] = fuzz.trimf(request_floor.universe, [0, 0, 5])
request_floor['medium'] = fuzz.trimf(request_floor.universe, [2, 5, 8])
request_floor['high'] = fuzz.trimf(request_floor.universe, [5, 10, 10])

# ลิฟต์ขึ้น
rule1 = ctrl.Rule(current_floor['low'] & request_floor['high'] & direction['move'], movement['up'])
rule2 = ctrl.Rule(current_floor['low'] & request_floor['medium'] & direction['move'], movement['up'])
rule3 = ctrl.Rule(current_floor['medium'] & request_floor['high'] & direction['move'], movement['up'])

# ลิฟต์ลง
rule4 = ctrl.Rule(current_floor['high'] & request_floor['low'] & direction['move'], movement['down'])
rule5 = ctrl.Rule(current_floor['medium'] & request_floor['low'] & direction['move'], movement['down'])
rule6 = ctrl.Rule(current_floor['high'] & request_floor['medium'] & direction['move'], movement['down'])

# ลิฟต์หยุดเมื่อชั้นปัจจุบันเท่ากับชั้นที่ร้องขอ
rule7 = ctrl.Rule(current_floor['low'] & request_floor['low'] & direction['stop'], movement['stop'])
rule8 = ctrl.Rule(current_floor['medium'] & request_floor['medium'] & direction['stop'], movement['stop'])
rule9 = ctrl.Rule(current_floor['high'] & request_floor['high'] & direction['stop'], movement['stop'])

# กำหนดกฎเพิ่มครอบคลุมทุกชั้น
rule10 = ctrl.Rule(current_floor['low'] & request_floor['low'] & direction['move'], movement['stop'])
rule11 = ctrl.Rule(current_floor['medium'] & request_floor['medium'] & direction['move'], movement['stop'])
rule12 = ctrl.Rule(current_floor['high'] & request_floor['high'] & direction['move'], movement['stop'])

# สร้างระบบฟัซซี่อีกครั้งด้วยกฎทั้งหมด
elevator_control = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])
elevator = ctrl.ControlSystemSimulation(elevator_control)


# 5. ทดสอบระบบ
elevator.input['current_floor'] = 0
elevator.input['request_floor'] = 0
elevator.input['direction'] = 1

# ตรวจสอบว่าอินพุตทั้งหมดอยู่ในช่วงของฟังก์ชันสมาชิก
try:
    elevator.compute()  # คำนวณผลลัพธ์
except ValueError as e:
    print(f"เกิดข้อผิดพลาดในการคำนวณ: {e}")
    exit(1)

# ตรวจสอบว่ามีผลลัพธ์สำหรับตัวแปร 'movement' หรือไม่
if 'movement' in elevator.output:
    print(f"Movement: {elevator.output['movement']}")
else:
    print("ไม่พบผลลัพธ์สำหรับตัวแปร 'movement' กรุณาตรวจสอบกฎและอินพุตอีกครั้ง")

# 6. สร้างกราฟ

# กราฟแสดง membership function ของ current_floor
current_floor.view()
plt.title('Membership Function of Current Floor')

# กราฟแสดง membership function ของ request_floor
request_floor.view()
plt.title('Membership Function of Request Floor')

# กราฟแสดง membership function ของ direction
direction.view()
plt.title('Membership Function of Direction')

# กราฟแสดง membership function ของ movement
movement.view()
plt.title('Membership Function of Movement')

# 7. กราฟแสดงผลลัพธ์ของการเคลื่อนที่
movement.view(sim=elevator)
plt.title('Resulting Movement of Elevator')
plt.show()