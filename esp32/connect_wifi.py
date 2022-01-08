from exception import *
import network
import time

#连接WiFi
def connectWifi(wlan,ssid:str, passwd:str, timeout:int = 8):
    if not wlan.isconnected():
        wlan.connect(ssid,passwd)
        start = time.time()
        end = start
        while not wlan.isconnected() and end - start < timeout:   #等待连接
            time.sleep_ms(20)
            end = time.time()
    if not wlan.isconnected():
        raise ConnectWifiTimeOutError

def keep_wifi(ssid:str, passwd:str, timeout:int = 8):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)   #激活网络
    while True:
        try:
            if not wlan.isconnected():
                connectWifi(wlan,ssid,passwd,timeout)
        except ConnectWifiTimeOutError as e:
            print("ConnectWifiTimeOutError")
        except Exception as e:
            print("Error:",e)
        finally:
            time.sleep_ms(20)

if __name__ == '__main__':
    keep_wifi("xxxxx","xxxxx")