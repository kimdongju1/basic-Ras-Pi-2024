import sys
import time
import RPi.GPIO as GPIO
import adafruit_dht
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
import board
from picamera2 import Picamera2

# Load the UI file
form_class = uic.loadUiType("mainwindow2.ui")[0]

# GPIO pins
RED_LED = 4
GREEN_LED = 5
BLUE_LED = 27
DHT_PIN = board.D23

# Segment display pins
segment_pins = {
    'a': 26,
    'b': 13,
    'c': 12,
    'd': 20,
    'e': 21,
    'f': 19,
    'g': 16,
    'dp': 6
}

com_pins = [22, 23, 24, 25]

# Number patterns for 7-segment display
number_patterns = [
    [1, 1, 1, 1, 1, 1, 0, 0],  # 0
    [0, 1, 1, 0, 0, 0, 0, 0],  # 1
    [1, 1, 0, 1, 1, 0, 1, 0],  # 2
    [1, 1, 1, 1, 0, 0, 1, 0],  # 3
    [0, 1, 1, 0, 0, 1, 1, 0],  # 4
    [1, 0, 1, 1, 0, 1, 1, 0],  # 5
    [1, 0, 1, 1, 1, 1, 1, 0],  # 6
    [1, 1, 1, 0, 0, 0, 0, 0],  # 7
    [1, 1, 1, 1, 1, 1, 1, 0],  # 8
    [1, 1, 1, 1, 0, 1, 1, 0]   # 9
]

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)

for pin in com_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# DHT sensor setup
dhtDevice = adafruit_dht.DHT11(DHT_PIN)

# Initialize Picamera2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
time.sleep(2)

def display_number(number):
    pattern = number_patterns[number]
    for seg, pin in segment_pins.items():
        GPIO.output(pin, pattern[ord(seg) - ord('a')])

def activate_common_pin(index):
    for i, pin in enumerate(com_pins):
        GPIO.output(pin, GPIO.HIGH if i == index else GPIO.LOW)

# PyQt5 Window class
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_red.clicked.connect(self.red_led_control)
        self.pushButton_green.clicked.connect(self.green_led_control)
        self.pushButton_blue.clicked.connect(self.blue_led_control)
        self.pushButton_coolant.clicked.connect(self.coolant_button_pressed)
        self.pushButton_exit.clicked.connect(self.exit_button_pressed)
        self.pushButton_capture.clicked.connect(self.capture_image)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(500)  # Update temperature every 0.5 seconds

    def red_led_control(self):
        GPIO.output(RED_LED, not GPIO.input(RED_LED))

    def green_led_control(self):
        GPIO.output(GREEN_LED, not GPIO.input(GREEN_LED))

    def blue_led_control(self):
        GPIO.output(BLUE_LED, not GPIO.input(BLUE_LED))

    def coolant_button_pressed(self):
        for _ in range(5):
            GPIO.output(BLUE_LED, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(BLUE_LED, GPIO.LOW)
            time.sleep(0.5)

    def exit_button_pressed(self):
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(BLUE_LED, GPIO.LOW)
        GPIO.cleanup()
        sys.exit()

    def capture_image(self):
        filename = f"capture_{int(time.time())}.jpg"
        picam2.capture_file(filename)
        print(f"Image saved as {filename}")

    def update_temperature(self):
        try:
            temperature = dhtDevice.temperature
            if temperature is not None:
                self.lcdNumber.display(temperature)
                # Display temperature on 7-segment display
                tens = temperature // 10
                ones = temperature % 10
                activate_common_pin(0)
                display_number(ones)
                time.sleep(0.005)
            if temperature >= 29:
                GPIO.output(RED_LED, GPIO.HIGH)
                GPIO.output(GREEN_LED, GPIO.LOW)
            else:
                GPIO.output(RED_LED, GPIO.LOW)
                GPIO.output(GREEN_LED, GPIO.HIGH)
        except RuntimeError as ex:
            print(ex.args[0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()