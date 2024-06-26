# title : seg03.py
# date : 2024-06-26
# desc : FND 제어 연습

# 버튼을 클릭하면 FND 출력 1자리숫자 변경

import RPi.GPIO as GPIO
import time

# 각 세그먼트와 공통 핀에 연결된 GPIO 핀 번호
segment_pins = {
    'a': 26,
    'b': 13,
    'c': 12,
    'd': 20,
    'e': 21,
    'f': 19,
    'g': 16,
    'dp': 6
}

com_pins = [5, 6, 13, 19]  # COM1, COM2, COM3, COM4 핀
btn_pin = 25  # 버튼 핀

# 숫자 표시에 사용할 값 리스트의 리스트
number_patterns = [
    [1, 1, 1, 1, 1, 1, 0, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1, 0],  # 2
    [1, 1, 1, 1, 0, 0, 1, 0],  # 3
    [0, 1, 1, 0, 0, 1, 1, 0],  # 4
    [1, 0, 1, 1, 0, 1, 1, 0],  # 5
    [1, 0, 1, 1, 1, 1, 1, 0],  # 6
    [1, 1, 1, 0, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1, 0],  # 8
    [1, 1, 1, 1, 0, 1, 1, 0]   # 9
]

GPIO.setmode(GPIO.BCM)

# 세그먼트 핀을 출력으로 설정
for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)

# 공통 핀을 출력으로 설정
for pin in com_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # 공통 핀 초기 상태를 LOW로 설정 (비활성화)

# 버튼 핀을 입력으로 설정
GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

current_number = 0

def display_number(number):
    pattern = number_patterns[number]
    for i, pin in enumerate(segment_pins.values()):
        GPIO.output(pin, pattern[i])

def activate_common_pin(index):
    for i, pin in enumerate(com_pins):
        if i == index:
            GPIO.output(pin, GPIO.HIGH)  # 활성화
        else:
            GPIO.output(pin, GPIO.LOW)  # 비활성화

try:
    while True:
        if GPIO.input(btn_pin) == GPIO.HIGH:  # 버튼이 눌렸을 때
            for com_index in range(4):  # 4개의 공통 핀을 순차적으로 활성화
                activate_common_pin(com_index)
                display_number(current_number)
                time.sleep(0.5)
            current_number = (current_number + 1) % 10  # 숫자를 증가시키고 0-9 사이에서 순환
except KeyboardInterrupt:
    print('FND OFF!')
finally:
    GPIO.cleanup()
