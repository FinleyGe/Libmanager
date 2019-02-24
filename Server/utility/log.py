# _*_ coding:utf-8 _*_
# Creator : 葛骏
# Overview : 提供日志处理，封装 logging 模块
import logging

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
        datefmt='%Y-%m-%d %A %H:%M:%S',
        filename='log.log'
    )
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def log_info(info):
    logging.info(info)


def log_error(error):
    logging.error(error)