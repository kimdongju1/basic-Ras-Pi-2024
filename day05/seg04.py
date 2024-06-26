# 숫자가 1111, 2222, 3333, 4444 순으로 뜨는것
import RPi.GPIO as GPIO
import time

# 세그먼트 핀 정의
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

# 공통 핀 정의
common_pins = [22, 23, 24, 25]

# 숫자 패턴 (a, b, c, d, e, f, g, dp 순서)
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

# GPIO 설정 초기화
GPIO.setmode(GPIO.BCM)

# 세그먼트 핀을 출력으로 설정
for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # 공통 음극에서는 LOW로 초기화

# 공통 핀을 출력으로 설정
for pin in common_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # 공통 음극에서는 HIGH로 초기화

def display_number(number, position):
    # 모든 공통 핀 비활성화
    for pin in common_pins:
        GPIO.output(pin, GPIO.HIGH)

    # 각 세그먼트 핀에 숫자 패턴 출력
    for seg_name, pin in segment_pins.items():
        GPIO.output(pin, number_patterns[number][list(segment_pins.keys()).index(seg_name)])

    # 해당 자리의 공통 핀 활성화
    GPIO.output(common_pins[position], GPIO.LOW)  # 공통 음극에서는 LOW로 활성화
    time.sleep(0.5)  # 잠깐 동안 유지
    GPIO.output(common_pins[position], GPIO.HIGH)  # 공통 음극에서는 HIGH로 비활성화

try:
    while True:
        # '1234' 순차적으로 표시
        numbers_to_display = [1, 2, 3, 4]

        for position, number in enumerate(numbers_to_display):
            display_number(number, position)

except KeyboardInterrupt:
    print('FND OFF!')
finally:
    GPIO.cleanup()
