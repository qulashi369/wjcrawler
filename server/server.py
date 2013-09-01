#-*-coding:utf-8

import sys
import os.path
import tornado.wsgi
import tornado.httpserver
from scripts.log import logger
import traceback
import app


if len(sys.argv) != 1:
    port = int(sys.argv[1])
else:
    port = 8000
base_dir = os.path.split(sys.argv[0])
sys.path.append(base_dir)
try:
    container = tornado.wsgi.WSGIContainer(app.app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
except:
    logger.error(traceback.format_exc())
