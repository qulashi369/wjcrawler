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
DATABASE_URL = 'mysql://crawler:crawlerpwd@localhost:3306/xiaoshuo?charset=utf8'

if is_production():
    pass
else:
    DEBUG = True
    TESTING = True
    LOG = 'log/app.log'
    LOG_LEVEL = logging.DEBUG

try:
    from local_config import *
except ImportError, e:
    pass
