#!/usr/bin/env python3
# *_* coding: UTF-8 *_*
# @File  : server_tcpip.py
# @Author: Frank1126lin
# @Date  : 2020/11/9

import socket
import queue
import os
import json
import time
import threading
from predict import predict, source

# 主线程开启服务，接收图片地址，返回推理结果json
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "172.19.17.212"
port = 2200
s.bind((host, port))
s.listen(5)
print(f"已开始监听@{host}:{port}")

q1 = queue.Queue(0) # 接收消息队列
q2 = queue.Queue(0) # 结果消息队列


def conn():
    while True:
        conn, addr = s.accept()
        print(f"@{addr[0]}:{addr[1]}来了")
        thm = threading.Thread(target=msg_handle, args=(conn, addr))
        thm.setDaemon(True)
        thm.start()


def msg_handle(conn, addr):
    "消息处理及队列管理"
    while True:
        msg = conn.recv(1024)
        msg = msg.decode("utf-8")
        print(f"@{addr[0]}说：{msg}")
        q1.put(msg)
        t1 = time.time()
        event.wait()
        result = q2.get()
        if result:
            t2 = time.time()
            print("推理用时：", (t2-t1)*1000, "ms")
            print(result)
            result = json.dumps(result)
            result = bytes(result, encoding = "utf-8")
            conn.send(result)


def handle():
    while True:
        file_name = q1.get()
        if file_name is None:
            continue
        file_path = os.path.join(source, file_name)
        if os.path.exists(file_path):
            rst, rst_img = predict(source=file_path)
        else:
            rst = {"result": "file doesn't exists."}
        q2.put(rst)
        event.set()

if __name__ == '__main__':
    event = threading.Event()
    th1 = threading.Thread(target=conn)
    th1.setDaemon(True)
    th2 = threading.Thread(target=handle)
    th2.setDaemon(True)
    th1.start()
    th2.start()





