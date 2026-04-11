from gpiozero import MotionSensor  # GPIO 장치 제어를 위한 모션 센서 라이브러리 임포트
import time  # 시간 지연을 위한 라이브러리 임포트
from picamera2 import Picamera2  # 라즈베리 파이 카메라 모듈 제어 라이브러리
import datetime  # 파일명에 사용할 날짜와 시간 정보를 얻기 위한 라이브러리

pirPin = MotionSensor(16)# GPIO 16번 핀을 신호 입력 핀으로 설정

picam2 = Picamera2()# 카메라 초기 설정 및 시작
camera_config = picam2.create_preview_configuration() # 기본 미리보기 설정 생성
picam2.configure(camera_config)  # 생성된 설정을 카메라에 적용
picam2.start() # 카메라 모듈 가동

try:
    while True: # 무한 루프 시작
        try:
            sensorValue = pirPin.value # 센서로부터 현재 상태 값 읽기 (감지 시 1, 미감지 시 0)
            
            if sensorValue == 1: # 움직임이 감지된 경우
                now = datetime.datetime.now() # 현재 시스템 날짜와 시간 획득
                print(now) # 터미널에 감지 시간 출력

                fileName = now.strftime('%Y-%m-%d %H:%M:%S')  # 파일 이름을 '년-월-일 시:분:초' 형식의 문자열로 변환
                
                picam2.capture_file(fileName + '.jpg')  # 지정된 파일명으로 JPEG 이미지 촬영 및 저장
                
                time.sleep(5.5) # 중복 촬영 방지 및 센서 안정화를 위한 5.5초 대기
                
        except:  # 에러가 발생했을 때 실행되는 코드
            pass # 그냥 넘어감

except KeyboardInterrupt: # 사용자가 Ctrl+C를 눌러 프로그램을 종료할 때 예외 처리
    pass # 프로그램 종료
