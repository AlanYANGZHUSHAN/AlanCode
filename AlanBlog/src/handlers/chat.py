
# -*- coding: utf-8  -*-
import logging
import tornado.web
from dbs import chat
import json


chat_db = None
def init_chat_tool(config):
    global chat_db
    chat_db = chat.DBINT(config)

class getClientInfoHandler(tornado.web.RequestHandler):
    def post(self):
        ret = {}
        body = self.request.body
        req = json.loads(body, encoding = 'utf-8')
        res = chat_db.get_client_info(req)
        ret = {
                'status' : res["status"],
                'result' : res["result"],
                'msg'    : res['msg']
                }
        self.write(json.dumps(ret))
