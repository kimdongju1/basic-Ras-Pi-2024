# 순차적으로 0000, 1111, 2222, 3333, 4444 .... 식으로 뜨는것
import RPi.GPIO as GPIO
import time

a = 26
b = 13
c = 12
d = 20
e = 21
f = 19
g = 16
dp = 6

btn = 25

# 각 세그먼트에 연결된 GPIO 핀 번호
segment_pins = {
    'a': a,
    'b': b,
    'c': c,
    'd': d,
    'e': e,
    'f': f,
    'g': g,
    'dp': dp
}

# 각 숫자에 대한 세그먼트 활성화 패턴 (a, b, c, d, e, f, g 순서)
number_patterns = {
    0: (1, 1, 1, 1, 1, 1, 0, 0),  # 숫자 0의 패턴
    1: (0, 1, 1, 0, 0, 0, 0, 0),  # 숫자 1의 패턴
    2: (1, 1, 0, 1, 1, 0, 1, 0),  # 숫자 2의 패턴
    3: (1, 1, 1, 1, 0, 0, 1, 0),  # 숫자 3의 패턴
    4: (0, 1, 1, 0, 0, 1, 1, 0),  # 숫자 4의 패턴
    5: (1, 0, 1, 1, 0, 1, 1, 0),  # 숫자 5의 패턴
    6: (1, 0, 1, 1, 1, 1, 1, 0),  # 숫자 6의 패턴
    7: (1, 1, 1, 0, 0, 0, 0, 0),  # 숫자 7의 패턴
    8: (1, 1, 1, 1, 1, 1, 1, 0),  # 숫자 8의 패턴
    9: (1, 1, 1, 1, 0, 1, 1, 0)   # 숫자 9의 패턴
}

GPIO.setmode(GPIO.BCM)

# 세그먼트 핀을 출력으로 설정
for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# 숫자 표시 함수
def display_number(number):
    for seg_name in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'dp']:
        GPIO.output(segment_pins[seg_name], number_patterns[number][list(segment_pins.keys()).index(seg_name)])

try:
    while True:
        for number in range(10):
            display_number(number)
            time.sleep(0.5)  # 숫자가 표시된 후 0.5초 동안 유지

except KeyboardInterrupt:
    print('FND OFF!')
    GPIO.cleanup()

