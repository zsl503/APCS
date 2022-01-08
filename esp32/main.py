from pn532 import Pn532
import time
from util import *
import _thread
from computer import Computer
from umqtt import simple as mqtt
import ujson
from connect_wifi import keep_wifi
VERIFY_BLOCK_LIST = [6]
            
def success_verify():
    print("success")
    computer.open()


def card_detection():
    pn = Pn532(tx=25, rx=26)
    pn.active()
    cur_card = None
    while True:
        try:
            uid = pn.get_uid()
            if uid is not None and cur_card != uid:
                cur_card = uid
                flag = True
                for i in VERIFY_BLOCK_LIST:
                    res = find_by_uid_block(uid, i)
                    time.sleep_ms(20)
                    if res is None or pn.verify(i,res[0],uid) is False:
                        flag = False
                        break
                    if pn.read_card(i) != res[1]:
                        flag = False
                        break
                if flag:
                    success_verify()
                    
            else:
                cur_card = uid
                time.sleep_ms(20)
        except Exception as e:
            print('card error',e)


def publish():
    global client
    if computer.status:
        status = 1
    else:
        status = 0
    send_mseg={"params":{"status":status},"method":"thing.service.property.post"}
    client.publish(topic="xxxxx",msg=str(send_mseg),qos=1,retain=False)

def wait_message():
    global client
    while True:
        try:
            client.wait_msg()
            
        except Exception as e:
            print('wait_message:',e)
            continue
    
    
def recv_message(topic,msg):
    params = ujson.loads(msg)["params"]
    state = params.get("switch")
    if state == 0:
        computer.close()
    elif state == 1:
        print(computer.status)
        computer.open()
    elif state == 2:
        computer.reset()

#_thread.start_new_thread(receiveMessage,())#开启多线程

computer = Computer()
client_id='xxxxx'
user_name='xxxxx'#用户名
user_password='xxxxx'#用户密码
server= "xxxxx"#阿里云物联网平台地址
port=1883
client = None

def connect_aliyun():
    while True:
        try:
            global client
            client = mqtt.MQTTClient(client_id=client_id, server=server, port=port, user=user_name, password=user_password, keepalive=60)
            client.connect()
            client.set_callback(recv_message)
            client.subscribe("xxxxx")
            while True:
                publish()
                time.sleep_ms(30)
        except Exception as e:
            print(e)
        time.sleep(10)

if __name__ == '__main__':
    _thread.start_new_thread(card_detection,())#开启多线程
    #_thread.start_new_thread(keep_wifi,("SCAU_2.4G","9scau2021"))#开启多线程
    _thread.start_new_thread(keep_wifi,("xxxxx","xxxxx"))#开启多线程
    _thread.start_new_thread(connect_aliyun,())