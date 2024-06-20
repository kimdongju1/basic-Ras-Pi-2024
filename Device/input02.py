import RPi.GPIO as GPIO
import time 

led = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(led, GPIO.OUT)

try:
	while True:
		user_input = input("o 또는 x 입력")
		if user_input == 'o':
			GPIO.output(led, False)
		elif user_input == 'x':
			GPIO.output(led, True)

except KeyboardInterrupt:
	GPIO.cleanup()
