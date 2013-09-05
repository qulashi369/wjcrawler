# coding: utf8

import logging

def is_production():
    #TODO  使用环境变量判断是否为生产环境
    return False

DEBUG = False
TESTING = False
SECRET_KEY = '%^&S*DUFtf2132&*(2g3]]'
PROPAGATE_EXCEPTIONS = True
LOG = '/var/log/applog/app.log'
LOG_LEVEL = logging.WARNING

if is_production():
    DATABASE_URL = 'mysql://crawler:crawlerpwd@localhost:3306/xiaoshuo?charset=utf8'
    DATABASE_URL = 'mysql://root@localhost:3306/xiaoshuo?charset=utf8'
else:
    DEBUG = True
    TESTING = True
    LOG = 'log/app.log'
    LOG_LEVEL = logging.DEBUG
    DATABASE_URL = 'mysql://root@localhost:3306/xiaoshuo?charset=utf8'
