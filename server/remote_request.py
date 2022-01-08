#-*- coding:utf-8 -*-
from flask import Flask, request
from flask_cors import cross_origin, CORS
from ComputerControl import ComputerControl
import json
app = Flask(__name__)

ipv6 = "None"
time = "None"
begin_time = "None"
shutdown = False
@app.route('/MyPC',methods = ["POST","GET"])
def req():
    global ipv6
    global time
    global begin_time
    global shutdown
    global computer
    try:
        if request.method == 'GET':
            fp = open('index.html',mode = 'r')
            html = fp.read()
            fp.close()
            return html

        else:
            print(request.form)
            status = '未运行'
            if computer.status():
                status = '正在运行...'
            if request.form.get("code") == "-1":
                data = {
                    "beginTime":begin_time,
                    "ipv6":ipv6,
                    "updateTime":time,
                    "runStatus":status
                }
                return json.dumps(data,ensure_ascii=False)
                
            elif request.form.get("code") == "0":
                begin_time = request.form.get("time")
                shutdown = False
                return "Success"
            elif request.form.get("code") == "1":
                ipv6 = request.form.get("ipv6")
                time = request.form.get("time")
                if shutdown:
                    shutdown = False
                    return "shutdown"
                else:
                    return "Success"
            elif request.form.get("code") == "2":
                if request.form.get("opt") == "shutdown":
                    shutdown = True
                return "Success"
            elif request.form.get("code") == "3":
                computer.close()
                return "静待大约8秒，设备将强制关机~"
            elif request.form.get("code") == "4":
                computer.reset()
                return "正在重启，请耐心等待..."
            elif request.form.get("code") == "5":
                computer.open()
                return "成功开机啦!"

    except Exception as e:
        print(e)
        
            

computer = ComputerControl(access_key_id='xxxxx',
                          access_key_secret='xxxxx',
                          iot_instance_id='xxxxx',
                          product_key='xxxxx',
                          device_name='xxxxx', )
if __name__ == "__main__":
    while True:
        try:
            CORS(app, supports_credentials=True)
            app.run(debug=False, host='0.0.0.0',port="152")
        except Exception as e:
            print(e)
