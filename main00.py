import time                                  # 시간 대기를 위한 라이브러리
import requests                              # 텔레그램 서버로 메시지 전송을 보내기 위한 라이브러리
from gpiozero import MotionSensor, LED       # PIR 센서와 LED를 제어하기 위한 라이브러리
from flask import Flask, render_template     # Flask와 HTML 템플릿 렌더링 기능
from threading import Thread                 # PIR 감지 루프를 백그라운드로 실행하기 위함
from datetime import datetime                # 현재 시각을 구하고 문자열로 변환하기 위함

# ===== 텔레그램 설정 =====
#토큰과 id는 다른사람에게 노출되면 안되므로 빈칸으로 저장함
my_token = ' '   # BotFather에게 발급받은 봇 토큰
telegram_id = ' '  # 메시지를 받을 내 텔레그램 chat_id

# ===== GPIO 설정 =====
pir = MotionSensor(16)     # GPIO 16번 핀에 연결된 PIR 센서 객체 생성 (움직임 감지용)
red_led = LED(21)          # GPIO 21번 핀에 연결된 빨간 LED 객체 생성 (침입자 감지 시 점등)
green_led = LED(20)        # GPIO 20번 핀에 연결된 초록 LED 객체 생성 (평상시/정상 상태 점등)

# ===== 현재 상태를 저장하는 딕셔너리 =====
# 이 딕셔너리 값을 PIR 감지 함수와 index.html이 공유해서 사용
status = {
    'state': '정상',          # 현재 상태 텍스트 ('정상' 또는 '감지됨')
    'last_detected': '없음',  # 마지막으로 감지된 시각
    'count': 0                # 누적 감지 횟수
}

# ===== Flask 웹 서버 생성 =====
app = Flask(__name__)   # Flask 앱 객체 생성

@app.route('/')   # 사용자가 루트 주소("/")로 접속했을 때 실행되는 함수 지정
def index():
    # templates/index.html 파일을 렌더링하면서 status 딕셔너리를 템플릿에 전달
    # → index.html 안에서 {{ status.state }} 같은 형식으로 값을 사용할 수 있음
    return render_template('index.html', status=status)

@app.route('/api/status')   # "/api/status" 주소로 접속하면 status를 JSON 형태로 그대로 반환
def api_status():
    return status

# ===== 텔레그램으로 메시지를 보내는 함수 =====
def send_telegram(message):
    # 텔레그램 Bot API의 sendMessage 엔드포인트 URL 구성
    url = f'https://api.telegram.org/bot{my_token}/sendMessage'
    # 전송할 데이터: 받는 사람(chat_id)과 메시지 내용(text)
    data = {'chat_id': telegram_id, 'text': message}
    try:
        requests.post(url, data=data)   # POST 방식으로 텔레그램 서버에 요청 전송
    except Exception as e:
        # 네트워크 오류 등으로 전송이 실패해도 프로그램이 멈추지 않도록 예외 처리
        print(f'Telegram error: {e}')

# ===== PIR 센서가 움직임을 감지했을 때 호출되는 콜백 함수 =====
def on_motion():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # 현재 시각을 "YYYY-MM-DD HH:MM:SS" 형식으로 변환

    # ----- 상태 정보 갱신 -----
    status['state'] = '감지됨'
    status['last_detected'] = now
    status['count'] += 1   # 감지 횟수 1 증가

    # ----- LED 제어: 초록 LED는 끄고 빨간 LED를 켬 (경고 표시) -----
    green_led.off()
    red_led.on()

    # ----- 텔레그램 알림 메시지 작성 및 전송 -----
    message = (
        f'🚨 침입자 감지!\n'
        f'시각: {now}\n'
        f'누적 감지 횟수: {status["count"]}회'
    )
    send_telegram(message)

    print(f'[Detected] {now}')   # 터미널에도 감지 로그 출력 (디버깅용, 영어로 출력해 인코딩 문제 방지)

# ===== PIR 센서가 움직임을 감지하지 않을 때(=평상시) 호출되는 콜백 함수 =====
def on_no_motion():
    status['state'] = '정상'   # 상태를 다시 '정상'으로 갱신

    # ----- LED 제어: 빨간 LED는 끄고 초록 LED를 켬 -----
    red_led.off()
    green_led.on()

    print('[Normal] No motion')   # 터미널 로그 출력

# ===== PIR 센서 감지를 계속 감시하는 함수 (별도 스레드에서 실행됨) =====
def pir_loop():
    green_led.on()   # 프로그램 시작 시 기본 상태는 '정상'이므로 초록 LED를 먼저 켜둠
    print('PIR sensor starting...')

    # gpiozero의 이벤트 콜백 등록: 움직임이 감지/해제될 때마다 자동으로 해당 함수가 호출됨
    pir.when_motion = on_motion
    pir.when_no_motion = on_no_motion

    # 이 스레드가 종료되지 않도록 무한 대기
    # (실제 감지 처리는 위에서 등록한 콜백이 백그라운드에서 알아서 수행함)
    while True:
        time.sleep(1)

# ===== 프로그램 진입점 =====
if __name__ == '__main__':
    # PIR 감지 루프를 메인 스레드와 별개로 동작하는 데몬 스레드로 실행
    # daemon=True로 설정하면 메인 프로그램이 종료될 때 이 스레드도 함께 종료됨
    t = Thread(target=pir_loop, daemon=True)
    t.start()

    print('Web server: http://<RaspberryPi IP>:5000')

    # Flask 웹 서버 실행
    # host='0.0.0.0' → 같은 네트워크의 다른 기기에서도 접속 가능하도록 모든 IP에서 접속 허용
    # port=5000      → 접속 포트 번호
    # debug=False    → 운영(시연)용으로 디버그 모드 비활성화
    app.run(host='0.0.0.0', port=5000, debug=False)
