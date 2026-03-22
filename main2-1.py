from gpiozero import LEDBoard #gpiozero 라이브러리에서 LEDBorad 클래스를 임포트
from time import sleep #time 라이브러리에서 sleep 클래스 임포트

leds = LEDBoard(2,3,4,20,21) #변수 이름이 leds인 LED묶음 생성후 사용할 GPIO번호 할당

try:
    while 1: #프로그램이 강제로 꺼질때까지 무한반복
        leds.value = (0,0,1,1,0) #GPIO 4,20번 3초동안 켜짐 나머지는꺼짐
        sleep(3.0) #sleep은 대기 시간을 설정
        leds.value = (0,1,0,1,0) #GPIO 3,20번 1초동안 켜짐 나머지는꺼짐
        sleep(1.0)
        leds.value = (1,0,0,0,1) #GPIO 2,21번 3초동안 켜짐 나머지는꺼짐
        sleep(3.0)
    
except KeyboardInterrupt: #ctrl + c 를 눌렀을때 실행되는 예외 처리
    pass #루프 중단후 프로그램종료

leds.off() #프로그램종료시 모든 LED 종료
