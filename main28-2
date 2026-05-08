import urllib.request    # 웹 요청 라이브러리
import json              # JSON 데이터를 처 라이브러리
import datetime          # 날짜와 시간 정보를 다루기 위한 라이브러리
import asyncio           # 비동기 프로그래밍(병렬 처리 등)을 위한 라이브러리
from telegram import Bot # 텔레그램 봇 조작을 위한 클래스

telegram_id = ''         # 메시지를 받을 사용자의 고유 Chat ID
my_token = ''            # 텔레그램 BotFather에게 받은 봇 인증 토큰
api_key = ''             # OpenWeatherMap에서 발급받은 API 서비스 키

bot = Bot(token=my_token)#토큰으로 봇 객체 생성

ALERT_HOURS = [7, 10, 13, 16, 19, 22]    # 알림 시간 목록
ALERT_TIMES = ["11:50", "17:58"]         # 알림시간 추가 지정

def getWeather():  # 날씨 정보를 가져와 문자열로 반환하는 함수
    url = f"https://api.openweathermap.org/data/2.5/forecast?q=Seoul&appid={api_key}&units=metric&lang=en&cnt=8" # 서울 24시간 예보 URL

    with urllib.request.urlopen(url) as r:  #API에 요청 보내기
        data = json.loads(r.read())         # JSON으로 변환

    text = ""           # 결과 문자열 초기화
    for i in range(8):  # 8개 시간대 순회 
        item = data['list'][i]               # i번째 날씨 데이터 가져오기
        hour = str((int(item['dt_txt'][11:13]) + 9) % 24).zfill(2)  # 시간 추출 후 KST 변환
        temp = item['main']['temp']          # 기온
        humi = item['main']['humidity']      # 습도
        desc = item['weather'][0]['description']        # 날씨 상태 설명
        text += f"({hour}h {temp}C {humi}% {desc})\n"   # 결과 문자열에 추가

    return text     # 완성된 날씨 문자열 반환

async def main():        # 비동기 메인 함수
    try:
        while True:        # 무한 반복
            지금 = datetime.datetime.지금()       # 현재 시간 가져오기
            hm = 지금.strftime('%H:%M')          # 현재 시각을 시:분 형식 문자열로 저장

            is_alert_hour = 지금.hour in ALERT_HOURS 및 지금.minute == 0 및 지금.second == 0      # 1. 정각 알림 조건 확인
            is_alert_time = hm in ALERT_TIMES 및 지금.second == 0    2. 지정 시각 알림 조건 확인

            if is_alert_hour 또는 is_alert_time:                # 알림 조건 중 하나라도 만족하면 메시지 전송
                msg = getWeather()                 # 날씨 데이터 가져오기
                print(msg)                         # 터미널에 출력
                await bot.send_message(chat_id=telegram_id, text=msg)       #텔레그램에 메시지 전송

            await asyncio.sleep(1)      #1초 대기후 반복

    except KeyboardInterrupt:
        # 사용자가 Ctrl+C를 눌러 프로그램을 종료할 때 예외 처리
        pass

# 비동기 메인 함수 실행
asyncio.run(main())
