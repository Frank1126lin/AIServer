#!/usr/bin/env python3
# *_* coding: UTF-8 *_*
# @File  : server_tcpip.py
# @Author: Frank1126lin
# @Date  : 2020/11/9

import socket
import queue
import os
import threading
from .predict import predict, source

# 主线程开启服务，接收图片地址，返回推理结果json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "192.168.2.200"
port = 2200
s.bind((host, port))
s.listen()
print(f"已开始监听@{host}:{port}")

q1 = queue.Queue(0) # 接收消息队列
q2 = queue.Queue(0) # 结果消息队列


def conn():
    while True:
        conn, addr = s.accept()
        print(f"@{addr[0]}:{addr[1]}来了")
        try:
            while True:
                msg = conn.recv(1024)
                if not msg:
                    continue
                msg = msg.decode("utf-8")
                q1.put(msg)
                print(f"@{addr[0]}说：{msg}")
                event.wait()
                result = q2.get()
                if result:
                    conn.send(result)
        except:
            print(f"@{addr[0]}:{addr[1]}走了")


def handle():
    while True:
        file_name = q1.get()
        if file_name is None:
            continue
        file_path = os.path.join(source, file_name)
        rst_txt, rst_img = predict(source=file_path)
        rst = {"result": rst_txt}
        q2.put(rst)
        event.set()

if __name__ == '__main__':
    event = threading.Event()
    th1 = threading.Thread(target=conn)
    th2 = threading.Thread(target=handle)
    # th3 = threading.Thread(target=handle)
    th1.start()
    th2.start()





