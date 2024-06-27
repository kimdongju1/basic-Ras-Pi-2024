# basic-Ras-Pi-2024

## 1일차 
- GPIO 설정함수 
    - GPIO.setmode(GPIO.BOARD) - wPi
    - GPIO.setmode(GPIO.BCM) - BCM
    - GPIO.setup(channel, GPIO.mode)
        - channel : 핀번호, mode : IN/OUT
    - GPIO.cleanup()

- GPIO 출력함수
    - GPIO.output(channel, state)
    - channel : 핀번호, state : HIGH/LOW or 1/0 or True/False

- GPIO 입력함수
    - GPIO.input(channel)
    - channel : 핀번호, 반환값 : H/L or 1/0 or T/F

- 시간지연 함수
    - time.sleep(secs)

- 리눅스 파이썬 컴파일 명령어 : python 파일이름.py
- 실행끝내기 : Ctrl + c
- 파일삭제 rm -fr 파일이름

## 2일차
- 가상환경 설치 python -m venv --system-site-packages env
- 가상환경 들어가기source ./env/bin/activate
    - 빠져나오는방법 : deactivate


## 3일차
- GPIO 핀번호 확인 : gpio readall

- 파일 복사 : cp 원파일이름 생성파일이름