# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview :   用户操作
from model import database as db
from config import *
from utility import log
class User(db.Users):
    def __init__(self):
        super(User,self).__init__()
        self.rtv = {
            "rtv": None
        }

    def is_login(self, id):
        user = self.find("users", "id", id)
        if user[IS_LOGIN] == "0":
            return False
        else:
            return True

    def is_admin(self):
        pass

    def login(self, pwd, id=None, email=None):
        if id:
            ret = self.find("users", "id", id)
            if not ret:
                self.rtv["rtv"] = '-2'
                log.log_error("Not register Error by {}".format(id))
            else:
                if ret[0][PWD] != pwd:
                    self.rtv["rtv"] = '-1'
                    log.log_error("Wrong Password Error by {}".format(id))
                elif ret[0][IS_LOGIN] != "0":
                    self.rtv["rtv"] = '-3'
                    log.log_error("Replicate login Error by {}".format(id))
                else:
                    if not self.update("users", "is_login", "1", "id", id):
                        self.rtv["rtv"] = '0'
                        self.rtv["rtv"]["data"] = ret
                        log.log_info("Success by {}".format(id))
                    else:
                        self.rtv["rtv"] = '-101'
                        log.log_error("Other Error from Database")
        elif email:
            ret = self.find("users", "email", email)
            if not ret:
                self.rtv["rtv"] = '-2'
                log.log_error("Not register Error by {}".format(email))
            else:
                if ret[0][PWD] != pwd:
                    self.rtv["rtv"] = '-1'
                    log.log_error("Wrong Password Error by {}".format(email))
                elif ret[0][IS_LOGIN] != "0":
                    self.rtv["rtv"] = '-3'
                    log.log_error("Replicate login Error by {}".format(email))
                else:
                    if not self.update("users", "is_login", "1", "email", email):
                        self.rtv["rtv"] = '0'
                        log.log_info("Success by {}".format(email))
                    else:
                        self.rtv["rtv"] = '-101'
                        log.log_error("Other Error from Database")
        else:
            self.rtv["rtv"] = '-100'
            log.log_error("Wrong Operate Type")

    def register(self, name, email, pwd, type):
        if not self.find("users", "email", email):
            ret = self.insert(name, email, pwd, type)
            if not ret:
                self.rtv["rtv"] = '0'
            else:
                self.rtv["rtv"] = '-101'
                log.log_error("Other Error from Database")
        else:
            self.rtv["rtv"] = '-1'
            log.log_error("replicate email address by {}".format(email))

    def logout(self, id,):
        ret = self.find("users", "id", id)
        if ret:
            if ret[IS_LOGIN] == "0":
                self.rtv["rtv"] = "-1"
            else:
                if not self.update("users", "is_login", 0, "id", id):
                    self.rtv["rtv"] = "0"
                else:
                    self.rtv["rtv"] = "101"

    def borrow_book(self, uid, book_id):
        book = self.find("books", "id", book_id)
        user = self.find("users", "id", uid)
        if self.is_login(uid):
            if book:
                if int(book[REMAIN]) >= 1:
                    if user[TYPE] == "0" or user[TYPE] == "1":
                        if user[BOOK_ID] == "-1":
                            self.update("books", "remain", str(int(book[REMAIN]) - 1), "id", book_id)
                            self.rtv["rtv"] = "0"
                        else:
                            self.rtv["rtv"] = "-2"
                    else:
                        self.rtv["rtv"] = "-3"
                else:
                    self.rtv["rtv"] = "-1"
            else:
                self.rtv["rtv"] = "-4"
        else:
            self.rtv["rtv"] = "-6"

    def return_book(self, uid, book_id):
        user = self.find("users", "id", uid)
        book_id = self.find("books", "id", book_id)
        if self.is_login(uid):
            if user[BOOK_ID] != "-1":
                if self.update("books", "remain", book_id[REMAIN] + 1, "id", book_id):
                    self.rtv["rtv"] = "0"
                else:
                    self.rtv["rtv"] = "-100"
            else:
                self.rtv["rtv"] = "-1"
        else:
            self.rtv["rtv"] = "-2"

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



