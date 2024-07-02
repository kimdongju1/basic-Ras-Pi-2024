import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import cv2
from PyQt5.QtGui import QImage, QPixmap

# 온도 센서 설정
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

# 7-세그먼트 설정
fndSegs = [26, 13, 12, 20, 21, 19, 16]
fndSels = [25, 24, 23, 22]

# LED 설정
RED_LED = 18
GREEN_LED = 5

# GPIO 설정
GPIO.setmode(GPIO.BCM)
for fndSeg in fndSegs:
    GPIO.setup(fndSeg, GPIO.OUT)
    GPIO.output(fndSeg, 0)

for fndSel in fndSels:
    GPIO.setup(fndSel, GPIO.OUT)
    GPIO.output(fndSel, 1)

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

def fndOut(data, sel):
    for i in range(0, 7):
        GPIO.output(fndSegs[i], data & (0x01 << i))
    for j in range(0, 4):
        if j == sel:
            GPIO.output(fndSels[j], 0)
        else:
            GPIO.output(fndSels[j], 1)

def display_temperature(temp):
    # 온도를 7-세그먼트 디스플레이에 표시
    digits = [int(d) for d in f"{temp:04d}"]
    for i in range(4):
        fndOut(digits[i], i)
        time.sleep(0.003)

def read_temperature():
    # DHT11 센서에서 온도 읽기
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temperature is not None:
        return temperature
    return 0

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('mainwindow.ui', self)
        
        # 버튼 클릭 시 카메라 피드 보기
        self.pushButton.clicked.connect(self.show_camera_feed)
        
        # 타이머 설정 (1초마다 온도 업데이트)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(1000)
    
    def update_temperature(self):
        temperature = read_temperature()
        self.lcdNumber.display(temperature)
        display_temperature(temperature)
        
        if temperature >= 40:
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
            self.ledLabel.setText("LED Status: RED")
            self.ledLabel.setStyleSheet("background-color: red; color: white;")
        else:
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.HIGH)
            self.ledLabel.setText("LED Status: GREEN")
            self.ledLabel.setStyleSheet("background-color: green; color: white;")
    
    def show_camera_feed(self):
        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # OpenCV 이미지 PyQt 이미지로 변환
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage)
