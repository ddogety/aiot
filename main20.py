from flask import Flask        # Flask 웹 서버 프레임워크 임포트
from gpiozero import LED       # 라즈베리 파이 GPIO 제어 라이브러리 임포트

app = Flask(__name__)          # Flask 앱 생성

red_led = LED(21)  # GPIO 21번 핀에 연결된 LED 객체 설정 

@app.route('/') # 기본 경로('/') 접속 시 실행
def flask():
    return "hello Flask"

@app.route('/ledon') # '/ledon' 경로로 접속했을 때 LED를 킴
def ledOn():
    red_led.on()           # LED 켜기
    return "<h1> LED ON </h1>" #브라우저에 결과 출력

@app.route('/ledoff') # '/ledoff' 경로로 접속했을 때 LED를 끔
def LedOff():
    red_led.off()              # LED 끄기
    return "<h1> LED OFF </h1>" #브라우저에 결과 출력

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = "80") #모든 IP(0.0.0.0)에서 80번 포트로 서버 실행
