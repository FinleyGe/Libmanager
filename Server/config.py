# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 服务端配置文件
# 切勿任意修改任何字段！

# 服务端运行端口
ip_port = ('127.0.0.1', 8888)
# backlog指定在拒绝链接前，操作系统可以挂起的最大连接数，该值最少为1，大部分应用程序设为5就够用了
backlog = 5
# 预定义的一些常量
ID = 0
NAME = 1
EMAIL = 2
PWD = 3
TYPE = 4
BORROW_ID = 5
IS_LOGIN = 6

BOOK_ID = 0
BOOK_NAME = 1
BOOK_AMOUNT = 2
BOOK_REMAIN = 3
IS_ABLED = 4

# 管理员注册验证码，可以由管理员（我是指服务器的总管理员）手动更改
CK_CODE = 'd47244a38419d8d10e778e0f0cd11554'