import RPi.GPIO as GPIO
import time

# 각 세그먼트에 연결된 GPIO 핀 번호
segment_pins = {
    'a': 26,
    'b': 13,
    'c': 12,
    'd': 20,
    'e': 21,
    'f': 19,
    'g': 16
}

# 각 세그먼트가 순차적으로 표시할 숫자 패턴 (a, b, c, d, e, f, g 순서)
number_patterns = [
    (0, 1, 1, 0, 0, 0, 0),  # 0
    (1, 1, 0, 1, 1, 0, 1),  # 1
    (0, 1, 1, 0, 1, 1, 0),  # 2
    (0, 1, 1, 1, 1, 0, 0),  # 3
    (1, 1, 0, 1, 0, 0, 1),  # 4
    (0, 0, 1, 1, 1, 0, 1),  # 5
    (0, 0, 1, 1, 1, 1, 1),  # 6
    (0, 1, 1, 0, 0, 0, 0),  # 7
    (0, 1, 1, 1, 1, 1, 1),  # 8
    (0, 1, 1, 1, 0, 1, 1)   # 9
]

# 공통 음극(com)에 연결된 GPIO 핀 번호
com_pins = [25, 24, 23, 18]  # com1, com2, com3, com4 순서

GPIO.setmode(GPIO.BCM)

# 세그먼트 핀을 출력으로 설정
for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # 초기에는 모든 세그먼트를 비활성화 상태로 설정

# 공통 음극 핀을 출력으로 설정
for pin in com_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # 공통 음극 핀을 LOW로 설정하여 활성화

try:
    while True:
        for com_index in range(len(com_pins)):
            current_number = com_index + 1  # com1은 숫자 1, com2는 숫자 2, ...
            for seg_name, pin in segment_pins.items():
                GPIO.output(pin, number_patterns[current_number][list(segment_pins.keys()).index(seg_name)])
            time.sleep(0.5)  # 숫자가 표시된 후 0.5초 동안 유지

except KeyboardInterrupt:
    print('FND OFF!')
    GPIO.cleanup()
