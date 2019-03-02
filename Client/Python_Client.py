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

class client(object):
    def logout(self):
        if not self.is_login:
            print("You are not logged!")
            return -2

        data["data"] = {
            "type": "logout",
            "data": {
                self.userdata
            }

        }


    def close(self):
        data["data"] = {
            "type": "close"
        }
        self.s.send(en_json(data))


    def login(self):
        o = input("Input 1 to use id or 2 to use email >:")
        uid = None
        email = None
        if o == "1":
            uid = input("id:")
        elif o == "2":
            email = input("email:")
        else:
            return self.login()
        pwd = md5(input("password:"))
        data["data"] = {
            "id": uid,
            "email": email,
            "pwd": pwd
        }
        self.s.send(en_json(data))
        rtv = de_json(self.s.recv(1024))
        if rtv["rtv"] == "0":
            print("Login Succeed!")
            self.userdata = rtv["rtv"]["data"]
            return 0
        elif rtv["rtv"] == "-1":
            print("Wrong Password!")
            return self.login()
        elif rtv["rtv"] == "-2":
            print("Wrong id or email")
            return self.login()
        elif rtv["rtv"] == "-3":
            print("Replicate Login")
            return 0
        else:
            return rtv


    def register(self):
        name = input("name:")
        email = input("email:")
        pwd = md5(str(input("password:")))
        rpwd = md5(str(input("password Again:")))
        type = input("Your UserType.(0 for normal, 1 for admin):")
        ck_code = None
        if type == "1":
            ck_code = input("Check Code(Get it from ServerAdmin):")
        elif type != "0" and type != "1":
            print("Wrong Type!")
            return self.register()
        if pwd != rpwd:
            print("Two passwords is not same!")
            return self.register()
        else:
            data["data"] = {
                "name": name,
                "email": email,
                "pwd": pwd,
                "type": type,
                "ck_code": ck_code
            }
        self.s.send(en_json(data))
        rtv = de_json(self.s.recv(1024))
        if rtv["rtv"] == "0":
            print("Register Success")
            return 0
        elif rtv["rtv"] == "-1":
            print("Wrong E-mail Address!")
            return -1
        elif rtv["rtv"] == "-2":
            print("Wrong Check Code!")
            return -2
        else:
            return rtv



    def __init__(self):
        '''
        ip = input("Server IP:")
        port = int(input("Server Port:"))
        '''
        ip = "127.0.0.1"
        port = 8888
        self.is_login = False
        self.userdata = None
        self.s = socket.socket()
        self.s.connect((ip, port))
        if de_json(self.s.recv(1024))["rtv"] == "1":
            print("Connect with Server!")
        else:
            print("Connect Failed!")

        while True:
            o = input(">:")
            data["type"] = o
            if o == "help" or o == "?":
                print("""
                        Command         |           Describe
                        help/?          |           Print help message
                        login           |           Login
                        exit            |           Logout if login and Exit the Client
                        register        |           Register
                        logout          |           Logout
                """)
            if o == "login":
                rtv = self.login()
                if rtv == 0:
                    self.is_login = True
                    continue
            elif o == "register":
                rtv = self.register()
                if rtv == 0:
                    continue

            elif o == "exit":
                if self.is_login:
                    self.logout()
                self.close()
            else:
                print("Unknown command. Input help or ? to get help information")
                continue


if __name__ == '__main__':
    c = client()