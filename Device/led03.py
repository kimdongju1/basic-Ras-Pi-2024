import RPi.GPIO as GPIO
import time

red_pin = 21
green_pin = 16
blue_pin = 20

switch = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)

try:
	while True:
		if GPIO.input(switch) == True:
			GPIO.output(red_pin, False)
			GPIO.output(green_pin, True)
			GPIO.output(blue_pin, True)
			
		if GPIO.input(switch) == True:
			GPIO.output(red_pin, True)
			GPIO.output(green_pin, True)
			GPIO.output(blue_pin, False)
			
		if GPIO.input(switch) == True:
			GPIO.output(red_pin, True)
			GPIO.output(green_pin, False)
			GPIO.output(blue_pin, True)
			 
			
			
			

except KeyboardInterrupt:
	GPIO.cleanup()
			
				
