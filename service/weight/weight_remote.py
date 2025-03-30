# 라즈베리파이 2 (구독자 - subscriber.py)
import paho.mqtt.client as mqtt
import time

# MQTT 브로커 설정
broker_address = "broker.hivemq.com"  # 공개 MQTT 브로커
port = 1883
topic = "raspberry10/service/weight"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))

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