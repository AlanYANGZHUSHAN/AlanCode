# _*- coding:utf-8 _*_
import socket
import MySQLdb
import MySQLdb.cursors
from time import ctime

class DBINIT(object):
    def __init__(self, config):
        self.config = config
        self.blog_conn = MySQLdb.connect(**self.config["blog_db"]) 
        self.socket = socket.socket(AF_INET, SOCK_STREAM)
        self.socket.bind((self.config['client']['HOST'], self.config['client']['PORT']))
        self.socket.listen(self.config['client']['LISTEN_CLIENT'])

    @property
    def conn_blog(self):
        self.blog_conn.cursorclass = MySQLdb.cursors.DictCursor
        self.blog_conn.ping(True)
        self.blog_conn.set_character_set('utf8')
        return self.blog_conn


    def get_client_info(self,req):
        res = {}
        res['status'] = 'FAIL'
        res['msg'] = ''
        try:
            with self.conn_blog as cur:
                sql_select_cmd = "select Id,last_online_time  from client_info_list where Id = %s"
                params = [req["start_date"]]
                cur.execute(sql_select_cmd,params)
                if cur.fetchone():
                    res['status'] = 'SUCCESS'
                else:
                    res['msg'] = 'not resgister'
                    
        except Exception,e:
            res['msg'] += str(e)
            logging.info('get client info  is fail')
        return res



    def listen_client(self,req):
        tcpClientSocket, addr = self.socket.accept()
        address = addr[0] + ':' + str(addr[1])
        while True:
            with self.conn_blog as cur:
                sql_select_cmd = "select from_Id,content,create_time where to_Id = %s"
                params = [req['to_Id']]
                cur.execute(sql_select_cmd,params)
                for row in cur.fetchall():
                    send_message ='[From'+row['from_Id']+ 'At'+row['create_time']+']>'+row['content']
                    tcpClientSocket.send(send_message)
            topInfo = tcpClientSocket.recv(1024)
            if  not topInfo:
                break
        tcpClientSocket.close()





    


