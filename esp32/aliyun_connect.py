import time
from umqtt import simple as mqtt
import ujson
import network
import _thread
from connect_wifi import connectWifi

def publish(client):
    while True:
        send_mseg={"params":{"status":1},"method":"thing.service.property.post"}
        client.publish(topic="xxxxx",msg=str(send_mseg),qos=1,retain=False)
        time.sleep(1)

def receiveMessage(client):
  while True:
    client.wait_msg()
    
#接收信息。接收到的信息是json格式，要进行解析。
def recvMessage(topic,msg):
    print(topic,msg)
    params = ujson.loads(msg)["params"]
    state = params.get("switch")
    if state == 1:
        pass

def connect():
    client_id='xxxxx'
    user_name='xxxxx'#用户名
    user_password='xxxxx'#用户密码
    SERVER= "xxxxx"#阿里云物联网平台地址
    PORT=1883
    client = mqtt.MQTTClient(client_id=client_id, server=SERVER, port=PORT, user=user_name, password=user_password, keepalive=60)
    client.connect()
    client.set_callback(recvMessage)#设置回调函数
    client.subscribe("xxxxx")#订阅主题
    receiveMessage(client)
    #publish(client)

if __name__ == "__main__":
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)   #激活网络
    connectWifi(wlan,"xxxxx","xxxxx")#开启多线程
    connect()
