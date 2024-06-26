# title : ioh024_FND02.py
# date : 2024-06-26
# desc : FND 제어 연습

# 버튼을 클릭하면 FND 출력 숫자 변경

import RPi.GPIO as GPIO
import time

a = 26
b = 13
c = 12
d = 20
e = 21
f = 19
g = 16
dp = 6

btn = 25

i = 0

led = [a,b,c,d,e,f,g,dp]

# 숫자 표시에 사용할 값 리스트의 리스트
set = [[0,1,1,0,0,0,0,0],[1,1,0,1,1,0,1,0],[1,1,1,1,0,0,1,0],[0,1,1,0,0,1,1,0],
[1,0,1,1,0,1,1,0],[1,0,1,1,1,1,1,0],[1,1,1,0,0,1,0,0],
[1,1,1,1,1,1,1,0],[1,1,1,1,0,1,1,0],[1,1,1,1,1,1,0,0]]

GPIO.setmode(GPIO.BCM)

for n in range(0,8):   # FND GPIO 설정
   GPIO.setup(led[n], GPIO.OUT)

GPIO.setup(btn, GPIO.IN)   # 버튼 GPIO 설정

#GPIO.setup(g, GPIO.OUT)
#GPIO.setup(dp, GPIO.OUT)

try:
   while True:
      if GPIO.input(btn) == True:   # button을 pull-down 저항 방식으로 연결 -> btn에 True(1)신호가 오면 실행
         GPIO.output(a, set[i][0])
         GPIO.output(b, set[i][1])
         GPIO.output(c, set[i][2])
         GPIO.output(d, set[i][3])
         GPIO.output(e, set[i][4])
         GPIO.output(f, set[i][5])
         GPIO.output(g, set[i][6])
         GPIO.output(dp, set[i][7])
         print('clicked')
         time.sleep(0.5)
         i += 1   # 숫자 증가를 위해 +1

      if i == 10:   # FND에 0이 출력되고 나서 다음에 1로 넘어갈 수 있도록 처리
         i = 0

except KeyboardInterrupt:
   print('FND OFF!')
   GPIO.cleanup()
