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

# 각 숫자에 대한 세그먼트 활성화 패턴 (a, b, c, d, e, f, g 순서)
number_patterns = {
    0: (1, 1, 1, 1, 1, 1, 0),
    1: (0, 1, 1, 0, 0, 0, 0),
    2: (1, 1, 0, 1, 1, 0, 1),
    3: (1, 1, 1, 1, 0, 0, 1),
    4: (0, 1, 1, 0, 0, 1, 1),
    5: (1, 0, 1, 1, 0, 1, 1),
    6: (1, 0, 1, 1, 1, 1, 1),
    7: (1, 1, 1, 0, 0, 0, 0),
    8: (1, 1, 1, 1, 1, 1, 1),
    9: (1, 1, 1, 1, 0, 1, 1)
}

com_pin = 25  # 공통 양극 핀

GPIO.setmode(GPIO.BCM)

# 세그먼트 핀을 출력으로 설정
for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# 공통 양극 핀을 출력으로 설정
#GPIO.setup(com_pin, GPIO.OUT)
#GPIO.output(com_pin, GPIO.HIGH)  # 공통 양극 핀을 HIGH로 설정 (공통 양극)

try:
    while True:
        for number in range(10):
            pattern = number_patterns[number]
            for i, pin in enumerate(segment_pins.values()):
                GPIO.output(pin, pattern[i])
            time.sleep(1)  # 1초 동안 숫자 표시
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
