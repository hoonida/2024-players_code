import time
import RPi.GPIO as GPIO
from encoder import Encoder
import liblo as OSC
import sys

# GPIO 설정
GPIO.setmode(GPIO.BCM)

# 엔코더 콜백 함수
def valueChanged(value, direction):
    # 출력: 새 값과 방향
    print("* 새 값: {}, 방향: {}".format(value, direction))

    # 오실레이터 주파수를 업데이트하기 위해 OSC 메시지 전송
    OSC.send(target, "/rnbo/inst/0/params/oscillator_frequency/normalized", value)
    

# OSC 주소 생성 함수
def create_osc_address(port):
    try:
        return OSC.Address("localhost", port)
    except OSC.AddressError as err:
        print(err)
        sys.exit()

# 초기 OSC 메시지 전송 함수
def send_initial_osc_message(target):
    OSC.send(target, "/rnbo/jack/transport/rolling", 1)

# 엔코더 인스턴스 생성
e1 = Encoder(26, 19, valueChanged)

# OSC 타겟 생성
target = create_osc_address(1234)

# 초기 OSC 메시지 전송
send_initial_osc_message(target)

try:
    while True:
        # 엔코더로부터 현재 값을 가져옴
        current_value = e1.getValue()
        

        # 현재 값을 출력
        print("현재 값은: {}".format(current_value))
        
        # 일시 정지
        time.sleep(0.5)
        
except Exception as e:
    print("오류 발생: {}".format(e))
finally:
    GPIO.cleanup()