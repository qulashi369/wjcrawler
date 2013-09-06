# coding: utf8

import logging
import os

def is_production():
    if os.environ.get('PRODUCTION_ENV'):
        return True
    return False

DEBUG = False
TESTING = False
SECRET_KEY = '%^&S*DUFtf2132&*(2g3]]'
PROPAGATE_EXCEPTIONS = True
LOG = '/var/log/applog/app.log'
LOG_LEVEL = logging.WARNING

print is_production()
print os.environ.get('PRODUCTION_ENV')

if is_production():
    DATABASE_URL = 'mysql://crawler:crawlerpwd@localhost:3306/xiaoshuo?charset=utf8'
else:
    DEBUG = True
    TESTING = True
    LOG = 'log/app.log'
    LOG_LEVEL = logging.DEBUG
    DATABASE_URL = 'mysql://root@localhost:3306/xiaoshuo?charset=utf8'
