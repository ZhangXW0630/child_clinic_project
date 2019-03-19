# -*- coding=utf-8 -*-
# coding=utf-8

from acupuncture_handlers import *

import json,pickle,time,re,Levenshtein,base64,datetime,random
import os.path
import requests
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options, parse_command_line


define("port", default=2288, help="run on the given port", type=int)


class MakeApp(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/lung/upload", UploadHandler),
            (r"/lung/api/upload", UploadApiHandler),
            (r"/lung/index", IndexHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret='71oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
            login_url='/shanghai/login'
        )
        super(MakeApp, self).__init__(handlers, **settings)


def main():
    parse_command_line()
    app = MakeApp()
    app.listen(options.port, address="0.0.0.0")
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
