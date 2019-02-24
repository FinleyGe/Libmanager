# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : Python 客户端
import socket
import json
import hashlib
data = {
    "type": str(),
    "data": {}
}

def de_json(data):  # 解json
    return json.loads(str(data, "utf-8"))


def en_json(data):  # 序列化为json
    return json.dumps(data).encode()


def md5(data):  # md5加密
    h = hashlib.md5()
    h.update(data.encode())
    return h.hexdigest()


def login():
    o = input("Input 1 to use id or 2 to use email >:")
    uid = None
    email = None
    if o == "1":
        uid = input("id:")
    elif o == "2":
        email = input("email:")
    else:
        return login()
    pwd = md5(input("password:"))
    data["type"] = "login"
    data["data"] = {
        "id": uid,
        "email": email,
        "pwd": pwd
    }


def register():
    name = input("name:")
    email = input("email:")
    pwd = md5(input("password:").encode())
    rpwd = md5(input("").encode())

def main():
    '''
    ip = input("Server IP:")
    port = int(input("Server Port:"))
    '''
    ip = "127.0.0.1"
    port = 8888
    s = socket.socket()
    s.connect((ip, port))
    if de_json(s.recv(1024))["rtv"] == "1":
        print("Connect with Server!")
    else:
        print("Connect Failed!")

    while True:
        o = input(">:")
        if o == "help" or o == "?":
            print("""
                    Command         |           Describe
                    help/?          |           Print help message
                    login           |           Login
                    exit            |           Exit the Client
            """)
        if o == "login":
            login()
        elif o=="register":
            register()
        s.send(en_json(data))
        print(de_json(s.recv(1024)))

if __name__ == '__main__':
    main()