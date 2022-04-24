print("""
@Author: W01f
@repo: https://github.com/W01fh4cker/HunterXray/
@version: 1.0
@time: 2022/4/12
 _   _             _               __  __                
| | | |_   _ _ __ | |_ ___ _ __    \ \/ /_ __ __ _ _   _ 
| |_| | | | | '_ \| __/ _ \ '__|____\  /| '__/ _` | | | |
|  _  | |_| | | | | ||  __/ | |_____/  \| | | (_| | |_| |
|_| |_|\__,_|_| |_|\__\___|_|      /_/\_\_|  \__,_|\__, |
                                                   |___/ 
""")
import requests
import json
import base64
import os
import hashlib
import re
import sys
import smtplib
import socket
import datetime
import configparser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

#获取config配置文件
def getConfig(section, key):
    config = configparser.ConfigParser()
    a = os.path.split(os.path.realpath(__file__))
    path = 'data.conf'
    config.read(path)
    return config.get(section, key)

# 通过hunter获取url地址
def traversal_and_query():
    global i
    global number
    number = 1
    i =0
    api_key = getConfig("data", "api-key")
    query_sentence = input("[*]请输入查询语法：")
    search = base64.urlsafe_b64encode(query_sentence.encode("utf-8"))
    search_result = str(search, 'utf8')
    page = input("[*]请输入所查询页码：")
    page_size = input("[*]请输入每页资产条数：")
    is_web = input("[*]请选择资产类型（资产类型，1代表web资产，2代表非web资产，3代表全部）：")
    print("[*]请耐心等待~")
    cookie = getConfig("data", "cookie")
    start_time = getConfig("data", "start_time")
    end_time = getConfig("data", "end_time")
    status_code = getConfig("data", "status_code")
    url = 'https://hunter.qianxin.com/openApi/search?api-key=' + str(api_key) + '&search=' + str(
        search_result) + '&page=' + str(page) + '&page_size=' + str(page_size) + '&is_web=' + str(
        is_web) + '&start_time=' + str(start_time) + '&end_time' + str(end_time) + '&status_code=' + str(status_code)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'Cookie': cookie
    }
    resp = requests.get(url=url, headers=headers)
    global res
    res = json.loads((resp.content).decode('utf-8'))
    global first_url
    for i in range(len(res["data"]["arr"])):
        try:
            # 为防止扫到敏感网站，如edu、gov，因此只通过url这一种方式
            its_url = res["data"]["arr"][i]["url"]  # 网址
            if its_url is None:
                pass
            else:
                first_url = str(its_url)
        except:
            i = i + 1

# 判断api调用时候的状态码
def check_code():
    if (res["code"] == 200):
        pass
    elif (res["code"] == 401):
        print("[×]起始时间参数格式错误，格式应为2021-01-01 00:00:00")
    elif (res["code"] == 401):
        print("[×]无权限，请检查您的api-key和cookie是否填写正确！")
    else:
        print("[×]其他错误，请联系sharecat2022@gmail.com。")

#保存初步的url到文件
def save_url():
    with open("url.txt", 'a+', encoding='utf-8') as f:
        f.write(first_url + '\n')

#判断url前面有没有http/https头，如果没有就加上http://
def check_url_format():
    with open("url.txt",'r') as f:
        ln = f.readlines()
        for j in ln:
            url = j.strip()
            if url[:7] == 'http://' or url[:8] == 'https://':
                pass
            else:
                url = 'http://' + str(url)
                with open("url.txt",'w') as f:
                    f.write(url + '\n')

# 对一个连接进行xray扫描
def xrayscan(targeturl,opfilename):
    scancommand="xray.exe webscan --basic-crawler {} --html-output {}.html".format(targeturl,opfilename)
    os.system(scancommand)

# 完成之后发送邮件
def send_msg():
    server = "smtp.qq.com"
    port = 465
    sender = getConfig("data", "sender")
    pw = getConfig("data", "pw")
    receivers = getConfig("data", "receivers")
    machine_name = socket.gethostname()
    msg_root = MIMEMultipart('mixed')
    msg_root['From'] = Header(f'{machine_name} <{sender}>')
    msg_root['Subject'] = Header(f'Message from {machine_name}', 'utf-8')

    mail_msg = f"""
	<html>
	  <body>
	  <p>[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]<br>
		 Message from {machine_name}</p>

	<p>Path: {os.getcwd()}<br>
	   Args: {' '.join(sys.argv)}</p>
       您的扫描任务已经完成，如果觉得本软件还不错的话请给个star，谢谢您！
       有任何问题、建议，可以联系邮箱sharecat2022@gmail.com或者直接在github上面提出issues，感谢您的每一个建议！祝您生活愉快！
                                                                    From W01fh4cker
	</body>
	</html>"""

    msg_root.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    smtp = smtplib.SMTP_SSL(server, port)
    smtp.login(sender, pw)
    smtp.sendmail(sender, receivers, msg_root.as_string())
    print("[√]发送成功")
    smtp.quit()

# 多次扫描
def multi_scan():
    with open("url.txt","r") as f:
        lines = f.readlines()
    for line in lines:
        targeturl = line.strip()
        try:
            opfilename=hashlib.md5(targeturl.encode("utf-8"))
            xrayscan(targeturl.strip(), opfilename.hexdigest())
        except Exception as e:
            print(e)
        f.close()
    print("[√]扫描完成")

def main():
    try:
        traversal_and_query()
        check_code()
        save_url()
        check_url_format()
        multi_scan()
        send_msg()
    except Exception as e:
        print(e)
        print("请先自查您的搜索语法、配置文件填写是否有问题！如果确认无误，请直接发邮件至sharecat2022@gmail.com或者提出issues！")
        return again()

def again():
    while True:
        again = input("[*]本次已经检测完毕，如果想要继续请输入y，退出请按n。")
        if again not in {"y", "n"}:
            print("[*]请输入y或n而不是其他字符，谢谢！")
        elif again == "n":
            return "[*]感谢您的使用！"
        elif again == "y":
            return main()
if __name__ == '__main__':
    main()
