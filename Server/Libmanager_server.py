# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 服务端主文件
import socket
import asyncio
import msvcrt
import threading
from config import *
from utility import data_operate as do
from utility import userOperate as user
from utility import log


class Server():
    def login(self, data):
        u = user.User()
        u.login(id=data["id"], email=data["email"], pwd=data["pwd"])
        return u.rtv

    def register(self):
        u = user.User()
        u.register()
        return u.rtv

    def logout(self):
        pass

    def __init__(self):  # 入口
        self.s = socket.socket()
        self.s.bind(ip_port)
        self.s.listen(backlog)
        log.log_info("Server is running on {0}:{1}".format(ip_port[0], ip_port[1]))
        loop = asyncio.get_event_loop()
        while True:
            loop.run_until_complete(self.server())

    async def server(self):  # 异步
        self.conn, self.addr = self.s.accept()
        self.conn.send(do.en_json({
            'rtv': '1'
        }))
        log.log_info("Connect with : {0}:{1}".format(self.addr[0], self.addr[1]))
        data = do.de_json(self.conn.recv(1024))
        if data["type"] == 'login':
            self.conn.send(do.en_json(self.login(data["data"])))
        elif data["type"] == 'register':
            self.conn.send(do.en_json(self.register(data["data"])))
        elif data["type"] == 'register':
            self.conn.send(do.en_json(self.logout(data["data"])))
        else:  # 错误的操作类型
            self.conn.send(do.en_json(
                {
                    "rtv": "-100"
                }
            ))
        self.conn.close()
        log.log_info("Close connect with : {0}:{1}".format(self.addr[0], self.addr[1]))

    def __del__(self):
        log.log_info("Server is closed")


if __name__ == '__main__':
    s = Server()


