# -*- coding: utf-8  -*-
import logging
import tornado.web
from dbs import home_page
import json

homepage_db = None
def init_homepage_tool(config):
    global homepage_db
    homepage_db = home_page.DBINIT(config)

class homePageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('home_page.html')

class getContentListHandler(tornado.web.RequestHandler):
    def post(self):
        ret = {}
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = homepage_db.get_content_list(req)
        ret = {
                'status' : res["status"],
                'result' : res["result"],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class addOneItemHandler(tornado.web.RequestHandler):
    def post(self):
        ret = {}
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        logging.info(req)
        res = homepage_db.add_one_item(req)
        logging.info(res)
        ret = {
                'status' : res["status"],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class addOneFileHandler(tornado.web.RequestHandler):
    def post(self):

        ret = {}
        req = self.request.files['file']
        res = homepage_db.add_one_file(req)
        logging.info(res)
        ret = {
                'status' : res["status"],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))

class picToEpsHandler(tornado.web.RequestHandler):
    def post(self):

        ret = {}
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = homepage_db.pic_to_eps(req)
        logging.info(res)
        ret = {
                'status' : res["status"],
                'To_fileName' : res['To_fileName'],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))
