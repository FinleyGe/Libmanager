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

    def get_user_data(self):
        data["type"] = "get_user_data"
        data["data"] = {
            "id": self.userdata[0]
        }
        self.s.send(en_json(data))
        rtv = de_json(self.s.recv(1024))
        self.userdata = rtv["rtv"][0]
        return self.userdata

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
        if rtv["rtv"] == "-1":
            print("Wrong Password!")
            return self.login()
        elif rtv["rtv"] == "-2":
            print("Wrong id or email")
            return self.login()
        elif rtv["rtv"] == "-3":
            print("Replicate Login")
            return -1
        else:
            print("Login Succeed!")
            self.userdata[0] = rtv["rtv"][0]
            return 0

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

    def logout(self):
        if not self.is_login:
            print("You are not logged!")
            return -2
        data["data"] = {
                "id": self.userdata[0]
            }
        self.s.send(en_json(data))
        rtv = de_json(self.s.recv(1024))
        print(rtv)
        if rtv["rtv"] == "0":
            print("Logout!")
            self.is_login = False
        else:
            print("Failed to Logout")

    def borrow_book(self):
        book_id = input("Book ID : ")
        if not book_id:
            return -1
        else:
            data["data"] ={
                "id": self.userdata[0],
                "book_id": book_id
            }
        self.s.send(en_json(data))
        ret = de_json(self.s.recv(1024))["rtv"]
        if ret == "0":
            print("Success")
            return 0
        elif ret == "-1":
            print("Book {} is run out".format(book_id))
            return -1
        elif ret == "-2":
            print("You had been borrowed a book")
            return -1
        elif ret == "-3":
            print("You are not allowed to borrow a book")
            return -1
        elif ret == "-4":
            print("No book id : {}".format(book_id))
        elif ret == "-5":
            print("This book ({}) is not allowed to borrow".format(book_id))
        elif ret == "-6":
            print("You are not login!")

    def return_book(self):
        if self.is_login:
            data["data"] = {
                "id": self.userdata[0],
            }
            self.s.send(en_json(data))
            rtv = de_json(self.s.recv(1024))["rtv"]
            if rtv == "0":
                print("Success")
                self.get_user_data()
                return 0
            elif rtv == "-1":
                print("You have nothing to return")
                return -1
            elif rtv == "-2":
                print("You are not login")
                return -1
        else:
            print("You are not login")
            return -1

    def ban_user(self):
        if self.is_login:
            id = input("Ban User id : ")
            data["data"] = {
                "id": self.userdata[0],
                "ban_id": id
            }
            self.s.send(en_json(data))
            rtv = de_json(self.s.recv(1024))["rtv"]
            if rtv == "0":
                print("Success")
                return 0
            elif rtv == "-1":
                print("A wrong id {}".format(id))
                return -1
            elif rtv == "-2":
                print("The user has been already banned !")
                return -1
            elif rtv == "-3":
                print("You are not login")
                return -1
            elif rtv == "-4":
                print("You are not admin!")
                return -1
        else:
            print("You are not login")
            return -1

    def ban_book(self):
        if self.is_login:
            id = input("Ban Book id : ")
            data["data"] = {
                "id": self.userdata[0],
                "book_id": id
            }
            self.s.send(en_json(data))
            ret = de_json(self.s.recv(1024))["rtv"]
            if ret == "0":
                print("Success")
                return 0
            elif ret == "-1":
                print("A wrong id {}".format(id))
                return -1
            elif ret == "-2":
                print("The user has been already banned !")
                return -1
            elif ret == "-3":
                print("You are not login")
                return -1
            elif ret == "-4":
                print("You are not admin!")
                return -1
        else:
            print("You are not login")
            return -1

    def add_book(self):
        if self.is_login:
            id = input("Book id : ")
            amount = input("how many (int) :")
            data["data"] = {
                "id": self.userdata[0],
                "book_id": id,
                "book_amount": amount
            }
            self.s.send(en_json(data))
            ret = de_json(self.s.recv(1024))["rtv"]
            if ret == "0":
                print("Success")
                return 0
            elif ret == "-1":
                print("A wrong id {}".format(id))
                return -1
            elif ret == "-2":
                print("You are not login")
                return -1
            elif ret == "-3":
                print("You are not admin!")
                return -1
        else:
            print("You are not login")
            return -1

    def add_new_book(self):
        if self.is_login:
            name = input("Book Name: ")
            amount = input("how many (int) :")
            data["data"] = {
                "id": self.userdata[0],
                "book_amount": amount,
                "book_name": name,
                "is_abled": 1
            }
            self.s.send(en_json(data))
            ret = de_json(self.s.recv(1024))["rtv"]
            if ret == "0":
                print("Success")
                return 0
            elif ret == "-1":
                print("You are not login")
                return -1
            elif ret == "-2":
                print("You are not admin!")
                return -1
        else:
            print("You are not login")
            return -1

    def print_detail(self):
        if self.is_login:
            self.get_user_data()
            print("""
            ID : {0}
            Name: {1}
            Email : {2}
            type : {3} (0 for normal, 1 for admin, 2 for vistor)
            borrowing : {4}
            """.format(self.userdata[0], self.userdata[1], self.userdata[2], self.userdata[4], self.userdata[5]))
            return 0
        else:
            print("You are not login")
            return -1

    def checkbooks(self):
        self.s.send(en_json(data))
        ret = de_json(self.s.recv(1024))["rtv"]
        for i in ret:
            print(
                """
                    *********************************
                    ID : {0}
                    Name : {1}
                    Remain:{2}/{3}
                    Allowed:{4} (0 for False, 1 for True)
                    *********************************
                """.format(i[0], i[1], i[3], i[2], i[4])
            )
    def __init__(self):
        '''
        ip = input("Server IP:")
        port = int(input("Server Port:"))
        '''
        ip = "127.0.0.1"
        port = 8888
        self.is_login = False
        self.userdata = [None]
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
                
                        Because of CMD's strange code(It usually uses GBK, but I usually use utf-8)
                        I must use English to Write this and all of the message.
                        Please Dont laugh at my inapt English!
                        
                        Command         |           Describe
                                        |
                        help/?          |           Print help message
                        login           |           Login
                        exit            |           Logout if login and Exit the Client
                        register        |           Register
                        logout          |           Logout
                        checkbooks      |           Print all books' infomation
                        borrow_book     |           borrow a book
                        return_book     |           Return a book
                        ban_user        |           ban a user by id. Only admin
                        ban_book        |           ban a book by id. Only admin
                        add_book        |           add a book's amount
                        add_new_book    |           add a new book
                        print_user      |           Print your detail
                """)
            elif o == "exit":
                if self.is_login:
                    data["type"] = "logout"
                    self.logout()
                data["type"] = "exit"
                self.close()
                print("Dicconnect")
                exit()
            elif o == "login":
                rtv = self.login()
                if rtv == 0:
                    self.is_login = True
                    self.print_detail()
                    continue
            elif o == "register":
                rtv = self.register()
                if rtv == 0:
                    continue
            elif o == "logout":
                self.logout()
            elif o == "checkbooks":
                self.checkbooks()
            elif o == "borrow_book":
                self.borrow_book()
            elif o == "return_book":
                self.return_book()
            elif o == "ban_user":
                self.ban_user()
            elif o == "ban_book":
                self.ban_book()
            elif o == "add_book":
                self.add_book()
            elif o == "add_new_book":
                self.add_new_book()
            elif o == "print_user":
                self.print_detail()
            else:
                print("Unknown command. Input help or ? to get help information")
                continue


if __name__ == '__main__':
    c = client()