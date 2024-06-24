# URL접속을  /led/on, /led/off로 접속하면 led를 on, off하는 웹페이지를 만들자
from flask import Flask
import RPi.GPIO as GPIO


led_pin = 21 

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

app = Flask(__name__)

@app.route("/led/on")
def led_on():
	GPIO.output(led_pin, GPIO.LOW)
	return "LED is ON" 

@app.route("/led/off")
def led_off():
	GPIO.output(led_pin, GPIO.HIGH)
	return "LED is OFF"


if __name__ == "__main__":
	try:
		app.run(host="0.0.0.0", port="10011", debug=True)
	except KeyboardInterrupt:
		GPIO.cleanup()

