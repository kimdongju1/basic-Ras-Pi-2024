import RPi.GPIO as GPIO
import time

# 0~9까지 1Byte hex값
fndDatas = [0x3f, 0x06, 0x5b, 0x4f, 0x66, 0x6d, 0x7d, 0x27, 0x7f, 0x6f]
fndSegs = [26, 13, 12, 20, 21, 19, 16] # a~g led pin
fndSels = [25, 24, 23, 22] # fnd 선택 pin

# GPIO 설정
GPIO.setmode(GPIO.BCM)
for fndSeg in fndSegs:
	GPIO.setup(fndSeg, GPIO.OUT)
	GPIO.output(fndSeg, 0)

for fndSel in fndSels:
	GPIO.setup(fndSel, GPIO.OUT)
	GPIO.output(fndSel, 1)

def fndOut(data, sel):				# 표현할 숫자를 입력으로 받아 segment에 
	for h in range(0, 50):
		for i in range(0, 7):				# a~f까지 on되는 led를 켠다
	#		GPIO.output(fndSegs[0], 0)
	#		GPIO.output(fndSegs[1], 1)
	#		GPIO.output(fndSegs[2], 1)
	#		GPIO.output(fndSegs[3], 0)
			GPIO.output(fndSegs[i], fndDatas[data] & (0x01 << i))
			for j in range(0, 4):
				if j==sel:
					GPIO.output(fndSels[j], 0)
				else :
					GPIO.output(fndSels[j], 1)
					
count = 0

try:
	while True:
		if count > 9999: # 카운트가 9999를 넘으면 0으로 초기화
			count = 0
			
		d1000 = count / 1000
		d100 = count % 1000 / 100
		d10 = count % 100 / 10
		d1 = count % 10 
		
		d = [d1, d10, d100, d1000]
		
		for i in range(3, -1, -1):		#  fnd 선택 for문
				fndOut(int(d[i]), i)				# byte표현 함수호출
				time.sleep(0.00001)
#				time.sleep(0.5)

		count += 1
		
except KeyboardInterrupt:
	GPIO.cleanup()
