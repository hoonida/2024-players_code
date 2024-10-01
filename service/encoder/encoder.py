import sys, os, time, logging, argparse

import RPi.GPIO as GPIO
import liblo as OSC

class Encoder:

    def __init__(self, leftPin, rightPin, callback=None):
        self.leftPin = leftPin
        self.rightPin = rightPin
        self.value = 0
        self.state = '00'
        self.direction = None
        self.callback = callback
        GPIO.setup(self.leftPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.rightPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.leftPin, GPIO.BOTH, callback=self.transitionOccurred)
        GPIO.add_event_detect(self.rightPin, GPIO.BOTH, callback=self.transitionOccurred)

    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.leftPin)
        p2 = GPIO.input(self.rightPin)
        newState = "{}{}".format(p1, p2)

        if self.state == "00": # Resting position
            if newState == "01": # Turned right 1
                self.direction = "R"
            elif newState == "10": # Turned left 1
                self.direction = "L"

        elif self.state == "01": # R1 or L3 position
            if newState == "11": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Turned left 1
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)

        elif self.state == "10": # R3 or L1
            if newState == "11": # Turned left 1
                self.direction = "L"
            elif newState == "00": # Turned right 1
                if self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)

        else: # self.state == "11"
            if newState == "01": # Turned left 1
                self.direction = "L"
            elif newState == "10": # Turned right 1
                self.direction = "R"
            elif newState == "00": # Skipped an intermediate 01 or 10 state, but if we know direction then a turn is complete
                if self.direction == "L":
                    self.value = self.value - 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
                elif self.direction == "R":
                    self.value = self.value + 1
                    if self.callback is not None:
                        self.callback(self.value, self.direction)
                
        self.state = newState

    def getValue(self):
        return self.value




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




def main(args):

    # GPIO 설정
    GPIO.setmode(GPIO.BCM)

    # 엔코더 콜백 함수
    def valueChanged(value, direction):

        value = (value % 51)
        
        # 출력: 새 값과 방향
        # print("* 새 값: {}, 방향: {}".format(value, direction))

        # 오실레이터 주파수를 업데이트하기 위해 OSC 메시지 전송
        OSC.send(target, "/rnbo/inst/0/params/oscillator_frequency/normalized", value/50.0)
        

    # 엔코더 인스턴스 생성
    e1 = Encoder(26, 13, valueChanged)
    # e1 = Encoder(4, 17, valueChanged)

    # OSC 타겟 생성
    target = create_osc_address(1234)

    # 초기 OSC 메시지 전송
    send_initial_osc_message(target)

    try:
        while True:
            # 엔코더로부터 현재 값을 가져옴
            current_value = e1.getValue()
            

            # 현재 값을 출력
            #print("현재 값은: {}".format(current_value))
            
            # 일시 정지
            time.sleep(0.5)
            
    except Exception as e:
        print("오류 발생: {}".format(e))
    finally:
        GPIO.cleanup()


if __name__ == '__main__':

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)