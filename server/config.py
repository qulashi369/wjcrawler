# coding: utf8

def is_production():
    #TODO  使用环境变量判断是否为生产环境
    return False

DEBUG = False
TESTING = False
SECRET_KEY = '%^&S*DUFtf2132&*(2g3]]'
PROPAGATE_EXCEPTIONS = True

if is_production():
    DATABASE_URI = 'mysql://crawler:crawlerpwd@localhost:3306/xiaoshuo?charset=utf8'
else:
    DEBUG = True
    TESTING = True
    DATABASE_URI = 'mysql://root@localhost:3306/xiaoshuo?charset=utf8'
