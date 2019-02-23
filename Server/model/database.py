# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 数据库操作文件
import sqlite3
import logging


class Database(object):
    def __init__(self):
        self.db = sqlite3.connect("database.db")
        self.db.execute("""create table if not exists users(
                            id integer primary key autoincrement,
                            name varchar(20) not null ,
                            email varchar UNIQUE not null,
                            pwd varchar not null,
                            type integer default 2,
                            book_id integer default -1,
                            book_date integer,
                            is_login integer default 0
                          )
                """)
        self.cur.execute("""
                create table if not exists books (
                    id integer primary key autoincrement,
                    name varchar(20) not null ,
                    type integer default 0,
                    amount integer not null ,
                    remain integer not null ,
                    is_abled integer default 1
                )
        """)


    def __del__(self):
        self.db.commit()
        self.db.close()
        logging.info("Database is closed")


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
        select * from {0} where {1} = ?
""".format(table, item), value)
        return ret.fetchall()


class Users(Database):
    def insert(self, name, email, pwd, type):
        ret = self.db.execute("""
                insert into users (name,email,pwd,type) values (?,?,?,?)
        """, (name, email, pwd, type))
        return ret.fetchall()


class Books(Database):
    def insert(self, name, type, amount, remain, is_abled):
        ret = self.db.execute("""
                insert into books (name,type,amount,remain,is_abled) values (?,?,?,?,?)
        """, (name, type, amount, remain, is_abled))
        return ret.fetchall()

