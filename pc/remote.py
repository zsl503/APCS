import os
import re
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import requests

is_send = False

def send_email(target_email, text):
    fromaddr = 'zsl503503@163.com'  # 邮件发送方邮箱地址
    password = 'SPUXTRVSZCONGGNB'  # 密码(部分邮箱为授权码)
    toaddrs = [target_email]  # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发

    # 设置email信息
    # ---------------------------发送字符串的邮件-----------------------------
    # 邮件内容设置
    message = MIMEText(text, 'plain', 'utf-8')
    # 邮件主题
    subject = "远程提醒"
    message['Subject'] = Header(subject, 'utf-8')
    # 发送方信息
    message['From'] = formataddr(["远程通知", fromaddr])
    message['To'] = formataddr(["用户", target_email])
    # 接受方信息
    # ---------------------------------------------------------------------

    # 登录并发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.163.com', 994)  # 163邮箱服务器地址，端口默认为25
        server.login(fromaddr, password)
        server.sendmail(fromaddr, toaddrs, message.as_string())
        print('success send to ' + target_email)
        server.quit()
        return True

    except smtplib.SMTPException as e:
        print('error send to ' + target_email, e)  # 打印错误
        return False


def getIPv6Address():
    try:
        output = os.popen("ipconfig /all").read()
        result = re.findall(r"(([a-f0-9]{1,4}:){7}[a-f0-9]{1,4})", output, re.I)
        return result[0][0]
    except Exception as e:
        return "Error"


def post_state(data):
    global is_send
    url = "http://101.34.186.93:152/MyPC"
    try:
        res = requests.post(url=url, data=data)
        if res.text == "shutdown":
            send_email("2240453009@qq.com", "电脑正在关机...")
            os.system('shutdown -s -f -t 0')
        is_send = False
        return
    except Exception as e:
        if is_send:
            return
        try:
            send_email("2240453009@qq.com", "无法发送数据到您的服务器！\n" + "ipv6:" + getIPv6Address())
        finally:
            print(e)
            is_send = True
            return


def get_data():
    time_tuple = time.localtime(time.time())
    time_str = "{}年{}月{}日 {}:{}:{}".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                           time_tuple[5])
    return {
        "code": "1",
        "time": time_str,
        "ipv6": str(getIPv6Address())
    }


if __name__ == "__main__":
    time_tuple = time.localtime(time.time())
    time_str = "{}年{}月{}日 {}:{}:{}".format(time_tuple[0], time_tuple[1], time_tuple[2], time_tuple[3], time_tuple[4],
                                           time_tuple[5])
    post_state({
        "code": "0",
        "time": time_str,
    })
    try:
        send_email("2240453009@qq.com", " 您的电脑已开机\n" + " ipv6:" + getIPv6Address())
    finally:
        while True:
            post_state(get_data())
            time.sleep(10)
