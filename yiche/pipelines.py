# -*- coding: utf-8 -*-

import MySQLdb
import MySQLdb.cursors
import logging
from twisted.enterprise import adbapi

class YichePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool(
                dbapiName ='MySQLdb',#数据库类型，我这里是mysql
                host ='127.0.0.1',#IP地址，这里是本地
                db = 'test',#数据库名称
                user = 'root',#用户名
                passwd = 'root',#密码
                cursorclass = MySQLdb.cursors.DictCursor,
                charset = 'utf8',#使用编码类型
                use_unicode = True
        )

    # pipeline dafault function
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        logging.debug(query)
        return item


    # 插入数据到数据库
    def _conditional_insert(self, tx, item):
        parms = (item['Date'],item['CarName'],item['Type'],item['SalesNum'])
        sql = "insert into yiche (Date,CarName,Type,SalesNum) values('%s','%s','%s','%s') " % parms
        logging.debug(sql)
        tx.execute(sql)
