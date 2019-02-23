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


        elif email:
            pass
        else:
            pass



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



