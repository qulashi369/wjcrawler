#-*-coding:utf-8

import sys
import os
os.environ['PRODUCTION_ENV'] = 'PRODUCTION'

import tornado.wsgi
import tornado.httpserver

import app


if len(sys.argv) != 1:
    port = int(sys.argv[1])
else:
    port = 8000


container = tornado.wsgi.WSGIContainer(app.app)
http_server = tornado.httpserver.HTTPServer(container)
http_server.listen(port)
tornado.ioloop.IOLoop.instance().start()
