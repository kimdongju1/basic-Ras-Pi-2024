import RPi.GPIO as GPIO
import time

pirPin = 24
led_Pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(pirPin, GPIO.IN)
GPIO.setup(led_Pin, GPIO.OUT)

try:
	while True:
		if GPIO.input(pirPin) == True:
				GPIO.output(led_Pin, False)
				print("Detected")
				time.sleep(0.5)

		elif GPIO.input(pirPin) == False:
			GPIO.output(led_Pin, True)

			
		

except KeyboardInterrupt:
	GPIO.cleanup()
