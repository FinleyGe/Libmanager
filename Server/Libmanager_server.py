# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 服务端主文件
import socket
import asyncio
import logging
import msvcrt
import threading
from config import *
from utility import data_operate as do


class Server():

    def login(self):
        pass

    def register(self):
        pass

    def logout(self):
        pass

    def __init__(self):  # 入口
        logging.basicConfig(filename="log.log")
        self.s = socket.socket()
        self.s.bind(ip_port)
        self.s.listen(backlog)
        logging.info("Server is running.")
        print("Server is running on {0}:{1}".format(ip_port[0], ip_port[1]))  # 启动服务器
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.server())

    async def server(self):  # 异步
        self.conn, self.addr = self.s.accept()
        self.conn.send(do.en_json({
            'rtv': '1'
        }))
        data = do.de_json(self.conn.recv(1024))
        print("Connect with : {0}:{1}".format(self.addr[0], self.addr[1]))
        logging.info("Connect with : {0}:{1}".format(self.addr[0], self.addr[1]))
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
        logging.info("Close connect with : {0}:{1}".format(self.addr[0], self.addr[1]))

    def __del__(self):
        logging.info("Server is closed")


if __name__ == '__main__':
    s = Server()


