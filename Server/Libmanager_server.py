# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 服务端主文件
import socket
import asyncio
from config import *
from utility import data_operate as do
from utility import userOperate as user
from utility import log


class Server(object):
    def login(self, data):
        u = user.User()
        u.login(id=data["id"], email=data["email"], pwd=data["pwd"])
        return u.rtv

    def register(self, data):
        u = user.User()
        if data["ck_code"] == CK_CODE or data["type"] == "0":
            u.register(data["name"], data["email"], data["pwd"], data["type"],)
            return u.rtv
        else:
            u.rtv["rtv"] = "-2"
            return u.rtv

    def logout(self, data):
        u = user.User()
        u.logout(data["id"])
        return u.rtv

    def borrow_book(self, data):
        u = user.User()
        u.borrow_book(data["id"], data["book_id"])
        return u.rtv

    def return_book(self, data):
        u = user.User()
        u.return_book(data["id"])
        return u.rtv

    def ban_user(self, data):
        u = user.User()
        u.ban_user(data["id"], data["ban_id"])
        return u.rtv

    def ban_book(self, data):
        u = user.User()
        u.ban_book(data["id"], data["book_id"])
        return u.rtv

    def add_book(self, data):
        u = user.User()
        u.add_book(data["id"], data["book_id"], data["book_amount"])
        return u.rtv

    def add_new_book(self, data):
        u = user.User()
        u.add_new_book(data["id"], data["book_name"], data["book_amount"], data["is_abled"])
        return u.rtv

    def checkbooks(self):
        u = user.User()
        u.checkbooks()
        return u.rtv

    def get_user_data(self, data):
        u = user.User()
        return {
            "rtv": u.find("users", "id", data["id"])
        }

    def clearlogin(self):
        u = user.User()

    def __init__(self):  # 入口
        self.clearlogin()
        self.s = socket.socket()
        self.s.bind(ip_port)
        self.s.listen(backlog)
        self.conn = None
        self.addr = None
        log.log_info("Server is running on {0}:{1}".format(ip_port[0], ip_port[1]))
        loop = asyncio.get_event_loop()
        while True:
            try:
                loop.run_until_complete(self.server())
            except Exception as e:
                log.log_error(e)

    async def server(self):  # 异步
        self.conn, self.addr = self.s.accept()
        self.conn.send(do.en_json({
            'rtv': '1'
        }))
        log.log_info("Connect with : {0}:{1}".format(self.addr[0], self.addr[1]))
        while True:
            data = do.de_json(self.conn.recv(1024))
            if data["type"] == 'login':
                self.conn.send(do.en_json(self.login(data["data"])))
            elif data["type"] == 'register':
                self.conn.send(do.en_json(self.register(data["data"])))
            elif data["type"] == 'logout':
                self.conn.send(do.en_json(self.logout(data["data"])))
            elif data["type"] == 'borrow_book':
                self.conn.send(do.en_json(self.borrow_book(data["data"])))
            elif data["type"] == 'return_book':
                self.conn.send(do.en_json(self.return_book(data["data"])))
            elif data["type"] == 'ban_user':
                self.conn.send(do.en_json(self.ban_user(data["data"])))
            elif data["type"] == 'ban_book':
                self.conn.send(do.en_json(self.ban_book(data["data"])))
            elif data["type"] == 'add_book':
                self.conn.send(do.en_json(self.add_book(data["data"])))
            elif data["type"] == 'add_new_book':
                self.conn.send(do.en_json(self.add_new_book(data["data"])))
            elif data["type"] == "checkbooks":
                self.conn.send(do.en_json(self.checkbooks()))
            elif data["type"] == "get_user_data":
                self.conn.send(do.en_json(self.get_user_data(data["data"])))
            elif data["type"] == "exit":
                log.log_info("Disconnect with : {0}:{1}".format(self.addr[0], self.addr[1]))
                self.conn.close()
                return 0
            else:  # 错误的操作类型
                self.conn.send(do.en_json(
                    {
                        "rtv": "-100"
                    }
                ))

    def __del__(self):
        log.log_info("Server is closed")


if __name__ == '__main__':
    s = Server()
