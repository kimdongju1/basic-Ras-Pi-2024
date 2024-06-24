from flask import Flask
import RPi.GPIO as GPIO

led_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

app = Flask(__name__)

@app.route("/")
def helle():
	return "Hello World"

@app.route("/led/<stack>")
if state == "on":
	GPIO.output(led_pin, GPIO.LOW)
elif state == "off":
	GPIO.output(led_pin, GPIO.HIGH)
elif state == "clear":
	GPIO.cleanup()
	return "GPIO Cleanup()"

if __name__=="__main__":
	try:
		app.run(host="0.0.0.0", port="10011", debug=True)
	except KeyboardInterrupt:
		GPIO.cleanup()
