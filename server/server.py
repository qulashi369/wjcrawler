#-*-coding:utf-8

import sys
import os.path
import tornado.wsgi
import tornado.httpserver
import app

port = int(sys.argv[1])
base_dir = os.path.split(sys.argv[0])
sys.path.append(base_dir)

container = tornado.wsgi.WSGIContainer(app.app)
http_server = tornado.httpserver.HTTPServer(container)
http_server.listen(port)
tornado.ioloop.IOLoop.instance().start()
