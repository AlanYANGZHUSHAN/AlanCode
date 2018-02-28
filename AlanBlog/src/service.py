# -*- coding: utf-8  -*-
import tornado.ioloop
import tornado.web
import tornado.httpserver
import logging
from handlers.home_page import *
#from handlers.chat import * 

def start_http(config):
    init_homepage_tool(config)
    #init_chat_tool(config)

    application = tornado.web.Application([
        (r'/static/(.*)', tornado.web.StaticFileHandler, {"path":config['static']}),
        (r"/homepage", homePageHandler),
        (r"/homepage/content/get", getContentListHandler),
        (r"/homepage/content/add", addOneItemHandler),
        (r"/homepage/content/addfile", addOneFileHandler),
        (r"/homepage/content/pictoeps", picToEpsHandler),
        ],
        debug = True
        )
    application.settings["template_path"] = config["templates"]
    server = tornado.httpserver.HTTPServer(application)
    server.listen(config["http_port"],config["http_host"])
    ioloop = tornado.ioloop.IOLoop.instance()
    print("ioloop start")
    ioloop.start()
