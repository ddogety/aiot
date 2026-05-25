import cv2                  # OpenCV 라이브러리 불러오기
from gpiozero import Buzzer # GPIO 부저 제어 클래스 불러오기
import time                 # 시간 관련 라이브러리 불러오기

buzzerPin = Buzzer(16)      # GPIO 16번 핀에 연결된 부저 초기화

def main():
    # 카메라 장치 연결
    camera = cv2.VideoCapture(-1)
    # 카메라 해상도 설정 (가로 640, 세로 480)
    camera.set(3, 640)
    camera.set(4, 480)

    face_xml = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'  # 얼굴 탐지 모델
    eye_xml = cv2.data.haarcascades + 'haarcascade_eye.xml'                   # 눈 탐지 모델
    face_cascade = cv2.CascadeClassifier(face_xml)                            # 얼굴 탐지 분류기 생성
    eye_cascade = cv2.CascadeClassifier(eye_xml)                              # 눈 탐지 분류기 생성

    # 카메라가 열려 있는 동안 반복
    while camera.isOpened():
        # 카메라에서 프레임 읽기
        _, image = camera.read()
        # 컬러 이미지를 그레이스케일로 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 그레이스케일 이미지에서 얼굴 탐지
        # scaleFactor: 이미지 축소 비율 / minNeighbors: 탐지 민감도 / minSize: 최소 얼굴 크기
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # 탐지된 얼굴 수 출력
        print("faces detected Number: " + str(len(faces)))

        # 얼굴이 1개 이상 탐지된 경우
        if len(faces):
            for (x, y, w, h) in faces:
                # 탐지된 얼굴에 파란색 사각형 표시
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

                # 얼굴 영역만 잘라내기 (그레이스케일 / 컬러)
                face_gray = gray[y:y+h, x:x+w]
                face_color = image[y:y+h, x:x+w]

                # 얼굴 영역 내에서 눈 탐지
                eyes = eye_cascade.detectMultiScale(
                    face_gray,
                    scaleFactor=1.1,
                    minNeighbors=5
                )

                # 탐지된 눈이 1개 이하이면 졸음 상태로 판단 → 부저 ON
                if len(eyes) <= 1:
                    buzzerPin.：()
                else:
                    # 눈이 정상적으로 2개 탐지되면 부저 OFF
                    buzzerPin.off()

                # 탐지된 눈에 초록색 사각형 표시
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(face_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        # 처리된 이미지를 화면에 출력
        cv2.imshow('result', image)

        # 'q' 키 입력 시 루프 종료
        if cv2.waitKey(1) == ord('q'):
            break

    # 모든 창 닫기 및 부저 종료
    cv2.destroyAllWindows()
    buzzerPin.off()

# 스크립트 직접 실행 시 main() 호출
if __name__ == '__main__':
    main()
