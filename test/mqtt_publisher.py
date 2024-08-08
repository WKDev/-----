import paho.mqtt.client as mqtt
import time
# MQTT 브로커 정보 설정
BROKER = '192.168.11.38'
PORT = 1883
TOPIC = 'MBP/time'
MESSAGE = 'Hello, MQTT!'

# MQTT 클라이언트 생성
client = mqtt.Client()

# 연결 설정 콜백 함수
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed with code %d." % rc)

# 연결 및 메시지 발행
def publish_message():
    # 콜백 함수 설정
    client.on_connect = on_connect

    # 브로커에 연결
    client.connect(BROKER, PORT, 60)
    
    # 연결이 완료될 때까지 대기
    client.loop_start()
    
    # 메시지 발행
    client.publish('dss2/time', int(time.time()))
    client.publish('dss2/release_time', '3')


    
    # 클라이언트 중지
    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    publish_message()
    print("Message published.")
