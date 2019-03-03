# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview :   用户操作
from model import database as db
from config import *
from utility import log


class User(db.Users):
    def __init__(self):
        super(User, self).__init__()
        self.rtv = {
            "rtv": str()
        }

    def is_login(self, id):
        user = self.find("users", "id", id)[0]
        if user[IS_LOGIN] == "0":
            return False
        else:
            return True

    def is_admin(self, id):
        user = self.find("users", "id", id)[0]
        if user[TYPE] == "1":
            return True
        else:
            return False

    def login(self, pwd, id=None, email=None):
        if id != None:
            ret = self.find("users", "id", id)[0]
            if not ret:
                self.rtv["rtv"] = '-2'
                log.log_error("Not register Error by {}".format(id))
            else:
                if ret[PWD] != pwd:
                    self.rtv["rtv"] = '-1'
                    log.log_error("Wrong Password Error by {}".format(id))
                    return 0
                if ret[IS_LOGIN] == "1":
                    self.rtv["rtv"] = '-3'
                    log.log_error("Replicate login Error by {}".format(id))
                else:
                    if not self.update("users", "is_login", "1", "id", id):
                        self.rtv["rtv"] = ret
                        log.log_info("Success by {}".format(id))
                    else:
                        self.rtv["rtv"] = '-101'
                        log.log_error("Other Error from Database")

        elif email != None:
            ret = self.find("users", "email", email)[0]
            if not ret:
                self.rtv["rtv"] = '-2'
                log.log_error("Not register Error by {}".format(email))
            else:
                print(ret)
                if ret[PWD] != pwd:
                    self.rtv["rtv"] = '-1'
                    log.log_error("Wrong Password Error by {}".format(email))
                    return 0
                if ret[IS_LOGIN] == "1":
                    print("-3")
                    self.rtv["rtv"] = '-3'
                    log.log_error("Replicate login Error by {}".format(email))
                else:
                    if not self.update("users", "is_login", "1", "email", email):
                        self.rtv["rtv"] = ret
                        log.log_info("Success by {}".format(email))
                    else:
                        self.rtv["rtv"] = '-101'
                        log.log_error("Other Error from Database")
        else:
            self.rtv["rtv"] = '-100'
            log.log_error("Wrong Operate Type")

    def register(self, name, email, pwd, type):
        if not self.find("users", "email", email)[0]:
            ret = self.insert(name, email, pwd, type)
            if not ret:
                self.rtv["rtv"] = '0'
            else:
                self.rtv["rtv"] = '-101'
                log.log_error("Other Error from Database")
        else:
            self.rtv["rtv"] = '-1'
            log.log_error("replicate email address by {}".format(email))

    def logout(self, id):
        ret = self.find("users", "id", int(id))[0]
        print(ret)
        if ret:
            if ret[IS_LOGIN] == "0":
                self.rtv["rtv"] = "-1"
            else:
                if not self.update("users", "is_login", 0, "id", id):
                    self.rtv["rtv"] = "0"
                else:
                    self.rtv["rtv"] = "101"

    def borrow_book(self, uid, book_id):
        book = self.find("books", "id", book_id)[0]
        user = self.find("users", "id", uid)[0]
        if self.is_login(uid):
            if book:
                if int(book[BOOK_REMAIN]) >= 1:
                    if user[TYPE] == "0" or user[TYPE] == "1":
                        if user[BORROW_ID] == "-1":
                            self.update("books", "remain", str(int(book[BOOK_REMAIN]) - 1), "id", book_id)
                            self.update("users", "book_id", book_id, "id", uid)
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

    def return_book(self, uid):
        user = self.find("users", "id", uid)[0]
        if self.is_login(uid):
            if user[BORROW_ID] != "-1":
                book = self.find("books", "id", user[BORROW_ID])[0]
                if not self.update("books", "remain", str(int(book[BOOK_REMAIN]) + 1), "id", book[BOOK_ID]):
                    self.update("users", "book_id", "-1", "id", uid)
                    self.rtv["rtv"] = "0"
                else:
                    self.rtv["rtv"] = "-101"
            else:
                self.rtv["rtv"] = "-1"
        else:
            self.rtv["rtv"] = "-2"

    def ban_user(self, id, ban_id ):
        user1 = self.find("users", "id", id)[0]
        user2 = self.find("users", "id", ban_id)[0]
        if self.is_admin(id):
            if self.is_login(id):
                if user2:
                    if user2[TYPE] == "2":
                        self.rtv["rtv"] = "-2"
                        return
                    if not self.update("users", "type", "2", "id", ban_id):
                        self.rtv["rtv"] = "0"
                    else:
                        self.rtv["rtv"] = "-101"
                else:
                    self.rtv["rtv"] = "-1"
            else:
                self.rtv["rtv"] = "-4"
        else:
            self.rtv["rtv"] = "-3"

    def ban_book(self, id, book_id):
        book = self.find("books", "id", book_id)[0]
        if self.is_login(id):
            if book[IS_ABLED]:
                if self.update("books", "is_abled", "1", "id", book_id):
                    self.rtv["rtv"] = "0"
                else:
                    self.rtv["rtv"] = "-101"
            else:
                self.rtv["rtv"] = "-2"
        else:
            self.rtv["rtv"] = "-3"

    def add_book(self, id, book_id, amount):
        user = self.find("users", "id", id)[0]
        book = self.find("books", "id", book_id)[0]
        if self.is_login(id):
            if self.is_admin(id):
                if book:
                    if self.update("books", "amount", str(int(book[BOOK_AMOUNT]) + amount), "id", book_id):
                        self.rtv["rtv"] = "0"
                    else:
                        self.rtv["rtv"] = "-101"
                else:
                    self.rtv["rtv"] = "-1"
            else:
                self.rtv["rtv"] = "-3"
        else:
            self.rtv["rtv"] = "-2"

    def add_new_book(self, id, book_name, book_amount, is_abled=0):
        user = self.find("users", "id", id)[0]
        if self.is_login(id):
            if self.is_admin(id):
                b = db.Books()
                if not b.insert(book_name, book_amount, is_abled):
                    self.rtv["rtv"] = "0"
                else:
                    self.rtv["rtv"] = "-101"
            else:
                self.rtv["rtv"] = "-1"
        else:
            self.rtv["rtv"] = "-2"

    def checkbooks(self):
        self.rtv["rtv"] = self.findall()

    def clear_login(self):
        super(User, self).clear_login()
