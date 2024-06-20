import RPi.GPIO as GPIO
import time

piezoPin = 13
melody = [130, 147, 165, 175, 196, 220, 247, 262]

GPIO.setmode(GPIO.BCM)
GPIO.setup(piezoPin, GPIO.OUT)

Buzz = GPIO.PWM(piezoPin, 440)

try:
	while True:
	user_input = input("숫자 입력")
	if user_input == '0','1','2','3','4','5','6','7'
		GPIO.output(melody):
			BUzz.ChangeFrequency
			time.sleep(0.3)




except KeyboardInterrupt:
	GPIO.cleanup()
