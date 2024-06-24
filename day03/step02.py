import RPi.GPIO as GPIO
import time

steps = [21, 22, 23, 24]
patterns = [
				[0, 0, 0, 1],
				[0, 0, 1, 1],
				[0, 0, 1, 0],
				[0, 1, 1, 0],
				[0, 1, 0, 0],
				[1, 1, 0, 0],
				[1, 0, 0, 0]
		]
GPIO.setmode(GPIO.BCM)

for stepPin in steps:
	GPIO.setup(stepPin, GPIO.OUT)
	GPIO.output(stepPin, 0)

try:
	while True:
		for pattern in patterns:
			for stepPin, value in zip(steps, pattern):
				GPIO.output(stepPin, value)
			time.sleep(0.01)

except KeyboardInterrupt:
	GPIO.cleanup()
