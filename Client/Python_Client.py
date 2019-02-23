# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : Python 客户端
import socket
import json
import hashlib


def de_json(data):  # 解json
    return json.loads(str(data, "utf-8"))


def en_json(data):  # 序列化为json
    return json.dumps(data).encode()


def md5(data):  # md5加密
    h = hashlib.md5()
    h.update(data)
    return h.hexdigest()


def main():
    ip = input("Server IP:")
    port = int(input("Server Port:"))
    s = socket.socket
    s.connect((ip, port))
    if de_json(s.recv(1024))["rtv"] == "1":
        print("Connect with Server!")
    else:
        print("Connect Failed!")

    while True:
            o = input(">:")


if __name__ == '__main__':
    main()