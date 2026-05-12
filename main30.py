import paho.mqtt.client as mqtt  # MQTT 라이브러리 임포트
import time                       # 시간 라이브러리 임포트
from gpiozero import LED          # GPIO 라이브러리의 LED 임포트

greenLed = LED(16)  # 초록 LED GPIO 16번 핀
blueLed = LED(20)   # 파랑 LED GPIO 20번 핀
redLed = LED(21)    # 빨강 LED GPIO 21번 핀

def on_message(client, userdata, msg):  # 메시지 수신 시 호출되는 함수
    print(msg.topic+" "+str(msg.payload))  # 토픽과 원본 페이로드 출력
    message = msg.payload.decode()         # 바이트 → 문자열 변환
    print(message)                         # 변환된 메시지 출력

    if message == "green_on":      # 메시지가 "green_on"이면
        greenLed.：()              # 초록 LED 켜기
    elif message == "green_off":   # 메시지가 "green_off"이면
        greenLed.off()             # 초록 LED 끄기
    elif message == "blue_on":     # 메시지가 "blue_on"이면
        blueLed.：()               # 파랑 LED 켜기
    elif message == "blue_off":    # 메시지가 "blue_off"이면
        blueLed.off()              # 파랑 LED 끄기
    elif message == "red_on":      # 메시지가 "red_on"이면
        redLed.：()                # 빨강 LED 켜기
    elif message == "red_off":     # 메시지가 "red_off"이면
        redLed.off()               # 빨강 LED 끄기

client = mqtt.Client()             # MQTT 클라이언트 객체 생성
client.on_message = on_message     # 메시지 수신 콜백 함수 등록
broker_address = "192.168.10.119"  # 브로커(라즈베리파이) IP 주소
client.connect(broker_address)     # 브로커에 연결
client.subscribe("led", 1)         # "led" 토픽 구독
client.loop_forever()              # 메시지 수신 대기
