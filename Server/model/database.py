# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 数据库操作文件
import sqlite3
from utility import log


class Database(object):
    def __init__(self):
        self.db = sqlite3.connect("database.db")
        self.db.execute("""
                create table if not exists users(
                    id integer primary key autoincrement,
                    name varchar(20) not null ,
                    email varchar UNIQUE not null,
                    pwd varchar not null,
                    type varchar default "2",
                    book_id varchar default "-1",
                    is_login varchar default "0"
                  )
                """)
        self.db.execute("""
                create table if not exists books (
                    id integer primary key autoincrement,
                    name varchar(20) not null ,
                    amount varchar not null ,
                    remain varchar not null ,
                    is_abled varchar default "1"
                )
        """)

    def __del__(self):
        self.db.commit()
        self.db.close()
        log.log_info("Database is closed")

    def delete(self, table, item, value):
        ret = self.db.execute("""
                delete from {0} where {1} = ?
        """.format(table, item), value)
        return ret.fetchall()

    def update(self, table, item, new_value, index, index_value):
        ret = self.db.execute("""
                update {0} set {1} = ? where {2} = ? 
        """.format(table, item, index), (new_value, index_value))
        return ret.fetchall()

    def find(self, table, item, value):
        ret = self.db.execute("""
        select * from {0} where {1} = "{2}"
        """.format(table, item, value))
        return ret.fetchall()

    def findall_users(self):
        ret = self.db.execute(
            """
                  select * from users
            """
        )

    def findall(self):
        ret = self.db.execute(
            """
                  select * from books
            """
        )
        return ret.fetchall()


class Users(Database):
    def insert(self, name, email, pwd, type):
        ret = self.db.execute("""
                insert into users (name,email,pwd,type) values (?,?,?,?)
        """, (name, email, pwd, type))
        return ret.fetchall()

    def clear_login(self):
        ret = self.db.execute("""
                        update users set is_login = 0
                """, (name, email, pwd, type))
        return ret.fetchall()

class Books(Database):
    def insert(self, name, amount, is_abled):
        ret = self.db.execute("""
                insert into books (name,amount,remain,is_abled) values (?,?,?,?)
        """, (name, amount, amount, is_abled))
        return ret.fetchall()
