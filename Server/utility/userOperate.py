# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview :   用户操作
from model import database as db
from config import *
class User(db.Users):
    def __init__(self):
        super(User,self).__init__()
        self.rtv={
            "rtv":None
        }

    def is_admin(self):
        pass

    def login(self, pwd, id=None, email=None ):
        if id:
            ret = self.find("users","id",id)
            if not ret:
                self.rtv["rtv"] = '-2'
            else:
                if ret[0][PWD] != pwd:
                    self.rtv["rtv"] = '-1'
                elif ret[0][IS_LOGIN] != "0":
                    self.rtv["rtv"] = '-3'
                else:
                    if not self.update("users", "is_login", "1", "id", id):
                        self.rtv["rtv"] = '0'
                    else:
                        self.rtv["rtv"] = '-101'
        elif email:
            ret = self.find("users", "email", email)
            if not ret:
                self.rtv["rtv"] = '-2'
            else:
                if ret[0][PWD] != pwd:
                    self.rtv["rtv"] = '-1'
                elif ret[0][IS_LOGIN] != "0":
                    self.rtv["rtv"] = '-3'
                else:
                    if not self.update("users", "is_login", "1", "email", email):
                        self.rtv["rtv"] = '0'
                    else:
                        self.rtv["rtv"] = '-101'
        else:
            self.rtv["rtv"] = '-100'

    def register(self):
        pass

    def logout(self):
        pass

    def borrow_book(self):
        pass

    def return_book(self):
        pass

    def ban_user(self):
        pass

    def ban_book(self):
        pass

    def add_book(self):
        pass

    def add_new_book(self):
        pass

    def delete_book(self):
        pass



