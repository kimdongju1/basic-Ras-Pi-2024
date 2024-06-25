from gpiozero import Button
from picamera2 import Picamera2
import time
import datetime

swPin = Button(26)

oldSw = 0
newSw = 0

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()


try:
	while True:	
		newSw = swPin.is_pressed
		if newSw != oldSw:
			oldSw = newSw

		if newSw ==1:
			now = datetime.datetime.now()
			print("now")
			fileName = now.strftime(' %Y-%m-%d %H:%M:%S ')
			picam2.capture_file(fileName + ' .jpg' )

		time.sleep(0.2)

except KeyboardInterrupt:
	pass
