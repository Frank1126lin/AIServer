#!/usr/bin/env python3
# *_* coding: UTF-8 *_*
# @File  : test.py
# @Author: Frank1126lin
# @Date  : 2020/11/1

import os
import time
import shutil
import socket
import threading

def s1():
    ss1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建socket对象
    host = socket.gethostbyname(socket.gethostname())# 获取本地主机名称
    # host = "192.168.2.200"
    port = 2200 # 定义端口号
    ss1.bind((host, port)) # 绑定端口号
    ss1.listen(5)
    print(f"@已开始监听@:{host}:{port}")
    global src_path
    src_path = "Z:\\"
    global tar_path
    tar_path = os.path.join(os.getcwd(),"china_photo", time.strftime("%Y-%m-%d", time.localtime(time.time())))
    if not os.path.exists(tar_path):
        os.makedirs(tar_path)
    while True:
        conn, addr = ss1.accept() # 建立客户端连接
        print(f"@{addr[0]}:{addr[1]}@来了")
        while True:
            m = conn.recv(1024)
            if not m:
                continue
            m = m.decode("utf-8")
            print(f"@{addr[0]}说：{m}")
            photo_name = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + ".bmp"
            # print(photo_name)
            if m == "CCD10":
                src_photo = os.path.join(src_path, "CCD10.bmp")
                tar_photo = os.path.join(tar_path, f"平整度-{photo_name}")
                if not os.path.exists(src_photo):
                    print("平整度图片不存在！请检查后重试！")
                    continue
                shutil.copy(src_photo, tar_photo)
                print("图片已保存至", tar_photo)
            if m == "CCD11":
                src_photo = os.path.join(src_path, "CCD11.bmp")
                tar_photo = os.path.join(tar_path, f"上外观-{photo_name}")
                if not os.path.exists(src_photo):
                    print("上外观图片不存在！请检查后重试！")
                    continue
                shutil.copy(src_photo, tar_photo)
                print("图片已保存至", tar_photo)
                event.set()


            if m == "CCD20":
                src_photo = os.path.join(src_path, "CCD20.bmp")
                tar_photo = os.path.join(tar_path, f"下外观-{photo_name}")
                if not os.path.exists(src_photo):
                    print("下外观图片不存在！请检查后重试！")
                    continue
                shutil.copy(src_photo, tar_photo)
                print("图片已保存至", tar_photo)


def s2():
    ss2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建socket对象
    host = socket.gethostbyname(socket.gethostname())# 获取本地主机名称
    # host = "192.168.2.200"
    port = 2100 # 定义端口号
    ss2.bind((host, port)) # 绑定端口号
    ss2.listen(5)
    print(f"@已开始监听@:{host}:{port}")
    conn, addr = ss2.accept() # 建立客户端连接
    print(f"@{addr[0]}:{addr[1]}@来了")
    while True:
        event.clear()
        m = conn.recv(1024)
        if not m:
            return
        print(f"@{addr[0]}说:{m}")
        msg = b"\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        event.wait()
        conn.send(msg)
        print(f"@{host}我说：{msg}")


if __name__ == '__main__':
    event = threading.Event()
    server_th = threading.Thread(target=s1)
    plc_th = threading.Thread(target=s2)
    server_th.start()
    plc_th.start()