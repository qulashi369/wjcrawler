# coding: utf8


# TODO 改密码，端口
DB_URL = 'mysql://crawler:crawlerpwd@localhost:3306/xiaoshuo_test?charset=utf8'

try:
    from local_config import *
except ImportError:
    pass
