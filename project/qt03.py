import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import RPi.GPIO as GPIO
import Adafruit_DHT
import cv2

# GPIO ����
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ���׸�Ʈ �� ����
segment_pins = {
    'A': 26,
    'B': 13,
    'C': 12,
    'D': 20,
    'E': 21,
    'F': 19,
    'G': 16,
    'DP': 6
}
com_pins = [22, 23, 24, 25]

for pin in segment_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

for pin in com_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

# LED �� ����
RED_LED = 18
GREEN_LED = 5
BLUE_LED = 27

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

# DHT11 ���� ����
DHT_PIN = 4
DHT_SENSOR = Adafruit_DHT.DHT11

# MainWindow Ŭ���� ����
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # UI ���� �ε�
        uic.loadUi("mainwindow.ui", self)
        
        # ��ư Ŭ�� �̺�Ʈ ����
        self.measureButton.clicked.connect(self.measure_temperature)
        self.captureButton.clicked.connect(self.capture_image)
        self.coolingButton.clicked.connect(self.activate_cooling)
        self.exitButton.clicked.connect(self.exit_application)

    def measure_temperature(self):
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            self.temperatureLabel.setText(f"Temperature: {temperature}��C")
            self.display_temperature(temperature)
            self.control_led(temperature)
        else:
            QMessageBox.warning(self, "Error", "Failed to retrieve data from sensor")

    def display_temperature(self, temperature):
        # ���׸�Ʈ ���÷��̸� �̿��Ͽ� �µ� ǥ�� (��: 23 -> "23")
        # �� �κ��� ���� �ϵ���� ���� �ڵ�� ��ü�Ǿ�� �մϴ�.
        pass

    def control_led(self, temperature):
        if temperature >= 40:
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
        else:
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.HIGH)

    def capture_image(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('capture.jpg', frame)
            QMessageBox.information(self, "Capture", "Image captured successfully")
        else:
            QMessageBox.warning(self, "Error", "Failed to capture image")
        cap.release()

    def activate_cooling(self):
        GPIO.output(BLUE_LED, GPIO.HIGH)

    def exit_application(self):
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(GREEN_LED, GPIO.LOW)
        GPIO.output(BLUE_LED, GPIO.LOW)
        GPIO.cleanup()
        sys.exit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
