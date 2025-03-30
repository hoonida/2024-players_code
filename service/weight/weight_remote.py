import sys, os
import argparse
import paho.mqtt.client as mqtt
import liblo as OSC
import json
import time


def main(args):

    # send all messages to port 1234 on the local machine
    try:
        target = OSC.Address(1234)
    except OSC.AddressError as err:
        print(err)    
        sys.exit()

    # start the transport via OSC
    OSC.send(target, "/rnbo/jack/transport/rolling", 1)


    # MQTT 브로커 설정
    broker_address = "broker.hivemq.com"  # 공개 MQTT 브로커
    port = 1883
    topic = "raspberry10/service/weight"

    def on_connect(client, userdata, flags, rc):
        if not args.service:
            print("Connected with result code "+str(rc))
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        if not args.service:
            print(msg.topic+" "+str(msg.payload.decode("utf-8")))

        dict = json.loads(msg.payload.decode("utf-8"))
        max_sum_weight = float(dict["max_sum_weight"])

        if not args.service:
            print(f"{max_sum_weight=}")

        OSC.send(target, "/rnbo/inst/0/params/weight_remote/normalized", max_sum_weight / 1000) ## kg 단위로 전송

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_address, port, 60)

    # 방법 2: loop_start()와 함께 사용
    client.loop_start()  # 백그라운드에서 스레드 시작
    try:
        while True:
            # 여기에 다른 코드를 추가할 수 있습니다
            time.sleep(1)
    except KeyboardInterrupt:
        print("프로그램 종료")
        client.loop_stop()
        client.disconnect()



if __name__ == "__main__":

    # Change the current working directory to the script directory
    dir_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(dir_path)

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--service', action='store_true')
    args = parser.parse_args()

    main(args)