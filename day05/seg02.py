import RPi.GPIO as GPIO
import time

# 세그먼트 핀 설정
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
switch_pin = 18  # 스위치 핀

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 	# 경고 메세지 비활성화

# 세그먼트 핀을 출력으로 설정
for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# 공통 양극 핀을 출력으로 설정
GPIO.setup(com_pin, GPIO.OUT)
GPIO.output(com_pin, GPIO.HIGH)  # 공통 양극 핀을 HIGH로 설정 (공통 양극)

# 스위치 핀을 입력으로 설정 (풀다운 저항 사용)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

current_number = 0

def display_number(number):
    pattern = number_patterns[number]
    for i, pin in enumerate(segment_pins.values()):
        GPIO.output(pin, pattern[i])

def switch_callback(channel):
    global current_number
    current_number = (current_number + 1) % 10
    display_number(current_number)

# 기존 이벤트 감지 제거
try:
	GPIO.remove_event_detect(switch_pin)
except RuntimeError:
	pass


# 스위치 이벤트 설정 (스위치를 누를 때마다 호출)
GPIO.add_event_detect(switch_pin, GPIO.RISING, callback=switch_callback, bouncetime=500)

try:
    display_number(current_number)  # 초기 숫자 표시
    while True:
        time.sleep(0.1)  # CPU 사용을 줄이기 위해 잠시 대기
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()



