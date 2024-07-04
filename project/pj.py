import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from picamera2 import Picamera2
import time
import RPi.GPIO as GPIO
import board
import adafruit_dht

# UI ���� �ε�
form_class = uic.loadUiType("mainwindow2.ui")[0]

# DHT11 ���� ����
DHT_PIN = 18
dhtDevice = adafruit_dht.DHT11(board.D18)

# ���׸�Ʈ �� ����
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

com_pins = [22, 23, 24, 25]  # COM1, COM2, COM3, COM4 ��

# ���� ǥ�ÿ� ����� �� ����Ʈ�� ����Ʈ
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

# LED �� ����
RED_LED = 4
GREEN_LED = 5
BLUE_LED = 27

GPIO.setmode(GPIO.BCM)

# ���׸�Ʈ ���� ������� ����
for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)

# ���� ���� ������� ����
for pin in com_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # ���� �� �ʱ� ���¸� LOW�� ���� (��Ȱ��ȭ)

# LED �� ����
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

# ī�޶� ����
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()
time.sleep(2)

def display_number(number, position):
    """�־��� ���ڸ� �־��� ��ġ�� ǥ���մϴ�."""
    pattern = number_patterns[number]
    for i, pin in enumerate(segment_pins.values()):
        GPIO.output(pin, pattern[i])

    # �ش� ��ġ�� ���� �� Ȱ��ȭ
    for i, pin in enumerate(com_pins):
        if i == position:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # UI�� ��ư ����
        self.pushButton_capture.clicked.connect(self.capture_image)
        self.pushButton_red.clicked.connect(lambda: self.control_led(RED_LED, True))
        self.pushButton_green.clicked.connect(lambda: self.control_led(GREEN_LED, True))
        self.pushButton_blue.clicked.connect(lambda: self.control_led(BLUE_LED, True))
        self.pushButton_exit.clicked.connect(self.exit_program)
        self.pushButton_coolant.clicked.connect(self.coolant)

        # Ÿ�̸� ����
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(1000)

        self.segment_timer = QTimer(self)
        self.segment_timer.timeout.connect(self.update_segment_display)
        self.segment_timer.start(5)

        self.current_temperature = 0
        self.current_com_pin = 2

    def capture_image(self):
        filename = f"capture_{int(time.time())}.jpg"
        picam2.capture_file(filename)
        print(f"Captured {filename}")

    def control_led(self, pin, state):
        GPIO.output(pin, state)

    def exit_program(self):
        GPIO.output(RED_LED, False)
        GPIO.output(GREEN_LED, False)
        GPIO.output(BLUE_LED, False)
        self.close()

    def coolant(self):
        for _ in range(10):
            GPIO.output(BLUE_LED, True)
            time.sleep(0.25)
            GPIO.output(BLUE_LED, False)
            time.sleep(0.25)

    def update_display(self):
        try:
            temp = dhtDevice.temperature
            humid = dhtDevice.humidity

            if temp is not None and humid is not None:
                self.current_temperature = temp
                self.lcdNumber.display(temp)

                # LED ����
                if temp >= 28:
                    GPIO.output(RED_LED, True)
                    GPIO.output(GREEN_LED, False)
                else:
                    GPIO.output(RED_LED, False)
                    GPIO.output(GREEN_LED, True)
            else:
                self.lcdNumber.display("Err")
        except RuntimeError as error:
            print(error.args[0])
        except Exception as error:
            dhtDevice.exit()
            raise error

    def update_segment_display(self):
        # �µ� ���� ���׸�Ʈ ���÷��̿� ǥ��
        temp = self.current_temperature
        tens = temp // 10
        units = temp % 10

        if self.current_com_pin == 2:
            display_number(tens, 2)  # COM3�� ���� �ڸ� ǥ��
            self.current_com_pin = 3
        else:
            display_number(units, 3)  # COM4�� ���� �ڸ� ǥ��
            self.current_com_pin = 2            
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
    GPIO.cleanup()