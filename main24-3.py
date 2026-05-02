import urllib.request, json, tkinter, tkinter.font  # 웹 요청, JSON 데이터처리, GUI 라이브러리 임포트

API_KEY = ""  # OpenWeatherMap API 키

def tick1Min():
    # 서울 날씨 API 요청 URL 생성
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Seoul&appid={API_KEY}&units=metric"
    
    with urllib.request.urlopen(url) as r:  # URL 열고 응답 받기
        data = json.loads(r.read())         # JSON 문자열 → 딕셔너리 변환
    
    temp = data["main"]["temp"]      # 온도 추출
    humi = data["main"]["humidity"]  # 습도 추출
    
    label.config(text=f"{temp:.1f}C   {humi}%")  # 라벨 텍스트 업데이트
    window.after(60000, tick1Min)                 # 1분 후 함수 재실행

window = tkinter.Tk()                    # 창 생성
window.title("TEMP HUMI DISPLAY")       # 창 제목 설정
window.geometry("400x100")              # 창 크기 설정 (가로400 x 세로100)
window.resizable(False, False)          # 창 크기 조절 비활성화
font = tkinter.font.Font(size=30)       # 폰트 크기 30
label = tkinter.라벨(window, text="", font=font)  # 텍스트 라벨 생성
label.pack()                            # 라벨을 창에 배치
tick1Min()                              # 시작시 날씨 조회 실행
window.mainloop()                       # 창 유지
