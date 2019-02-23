# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 提供一系列数据操作
import json
import hashlib


def de_json(data):  # 解json
    return json.loads(str(data, "utf-8"))


def en_json(data):  # 序列化为json
    return json.dumps(data).encode()


def md5(data):  # md5加密
    h = hashlib.md5()
    h.update(data)
    return h.hexdigest()

