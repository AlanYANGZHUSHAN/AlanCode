# -*- coding: utf-8  -*-
import logging
import MySQLdb
import MySQLdb.cursors
import datetime
import json
from PIL import Image
import os

class DBINIT(object):
    def __init__(self, config):
        self.config = config
        self.blog_conn = MySQLdb.connect(**self.config["blog_db"]) 

    @property
    def conn_blog(self):
        self.blog_conn.cursorclass = MySQLdb.cursors.DictCursor
        self.blog_conn.ping(True)
        self.blog_conn.set_character_set('utf8')
        return self.blog_conn


    def get_content_list(self, req):
        res = {}
        result_list = []
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['result'] = result_list
        req["start_date"] += ' 00:00:00'
        req["end_date"] += ' 23:59:59'
        try:
            with self.conn_blog as cur:
                if req['tag'] != '--select tag--':
                    sql_select_cmd = "select id,title,create_time,author,tag,url from content_list where create_time >= %s and create_time <= %s and tag = %s"
                    params = [req["start_date"], req["end_date"],req['tag']]
                else:
                    sql_select_cmd = "select id,title,create_time,author,tag,url from content_list where create_time >= %s and create_time <= %s"
                    params = [req["start_date"], req["end_date"]]
                cur.execute(sql_select_cmd, params)
            for row in cur.fetchall():
                item = {}
                item["id"] = row["id"]
                item["title"] = row["title"]
                item["create_time"] = row["create_time"].strftime('%Y-%m-%d %H:%M:%S')
                item["author"] = row["author"]
                item["tag"] = row["tag"]
                item["url"] = row["url"]
                result_list.append(item)
            res['result'] = result_list
            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('get content list is fail')
        return res

    def add_one_item(self, req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        if req['tag'] == '--select tag--':
            res['msg'] += "please select tag"
            return res
        try:
            with self.conn_blog as cur:
                sql_del_cmd = "delete from content_list where url = %s"
                params = [req["url"]]
                cur.execute(sql_del_cmd, params)
                sql_insert_cmd = "insert ignore into content_list(title, author, tag, url) values (%s,%s,%s,%s)"
                params = [req["title"], req["author"], req["tag"], req["url"]]
                cur.execute(sql_insert_cmd, params)

            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('add one item is fail')
        return res

    def add_one_file(self, req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        try:
            for item in req:
                f = open(self.config["static"]+'/myhtml/'+item['filename'],"w")
                f.write(item['body'])
                f.close()

            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('add one file is fail')
        return res


    def pic_to_eps(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        res['To_fileName'] = ''
        try:
            file_path = self.config["static"]+'/myhtml/'
            logging.info(file_path)
            logging.info(req['From_fileName'])
            img = Image.open(file_path+req['From_fileName'])
            img=img.convert("RGB")
            res['To_fileName'] = os.path.splitext(req['From_fileName'])[0]+'.eps'
            logging.info(res['To_fileName'])
            img.save(file_path+res['To_fileName'])
            res['status'] = 'SUCCESS'
        except Exception,e:
            res['msg'] += str(e)
            logging.info('pic to eps is fail')
        return res



