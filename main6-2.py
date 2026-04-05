from gpiozero import DigitalInputDevice  # 디지털 입력 장치를 사용하기 위한 라이브러리
from gpiozero import OutputDevice  # 디지털 출력 장치를 사용하기 위한 라이브러리
import time # 시간 지연을 위한 라이브러리

bz = OutputDevice(18)  # GPIO 18번 핀에 연결된 부저를 출력 장치로 설정
gas = DigitalInputDevice(17) # GPIO 17번 핀에 연결된 가스 센서를 입력 장치로 설정

try: #에러 또는 예외가 발생했을 때 정해둔 코드로 처리해주는 역할
    while True: #무한 반복
        if gas.value == 0:#가스가 감지 되었을 때
            print("gas")#gas를 화면에 출력
            bz.on()#부저가 울림
        else:#감지되지 않았을 때
            print("save")#save를 화면에 출력
            bz.off()#부저가 울리지 않음

        time.sleep(0.2)#빠른 동작을 방지하기 위해 0.2초간 대기

except KeyboardInterrupt:#try문의 예외처리 : Ctrl + C를 눌렀을 때 실행
    pass#프로그램 종료

bz.off()#프로그램 종료시 부저도 종료
