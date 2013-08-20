# coding: utf8


# TODO 改密码，端口
DB_URL = 'mysql://crawler:crawlerpwd@localhost:3306/xiaoshuo'

try:
    from local_config import *
except ImportError:
    pass
