import RPi.GPIO as GPIO
import time

piezoPin = 13
melody = [130, 147, 165, 175, 196, 220, 247, 262]

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

Buzz = GPIO.PWM(piezoPin, 440)

try:
	while True:
		user_input = input("숫자 입력:")
		if user_input.isdigit():
			index = int(user_input)
			if 0 <= index <= 7:
				Buzz.start(50)
				Buzz.ChangeFrequency(melody[index])
				time.sleep(0.3)
				Buzz.stop()
			else:
				print("0과 7사이값 입력")
		else:
			print("0과 7사이값 입력")




except KeyboardInterrupt:
	GPIO.cleanup()
