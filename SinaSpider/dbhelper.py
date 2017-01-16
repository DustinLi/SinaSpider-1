# encoding=utf-8

import pymysql
import logging
import time
import math
from messages import system_message
from sys import stdout
from items import SysLogItem

logid = math.floor(time.time())

class DBHelper(object):
    hostName = "localhost"
    dbUser = "root"
    dbPwd = "root"
    dbName = "weibo"
    dbCharset = "utf8"

    def __init__(self):
        try:
            self.conn = pymysql.Connect(host=self.hostName,
                                        user=self.dbUser,
                                        password=self.dbPwd,
                                        db=self.dbName,
                                        charset=self.dbCharset)
            self.dbcursor = self.conn.cursor()
            self.writeLog(system_message[10001])
        except:
            self.writeLog(system_message[11001], 'ERROR')
            raise

    def getConnection(self):
        return self.conn

    def getCursor(self):
        return self.dbcursor

    def executeSQL(self, sql, args=None):
        try:
            # print sql
            if args is None:
                er = self.dbcursor.execute(sql)
            else:
                er = self.dbcursor.execute(sql, args)
            self.conn.commit()
            return er
        except:
            self.writeLog(system_message[11002] + sql, 'ERROR')
            raise

    def selectItem(self, tableName, filter):
        whereClause = self.getWhereClause(filter)
        sql = "SELECT * FROM %s WHERE %s" % (tableName, whereClause)
        self.executeSQL(sql)
        return self.dbcursor.fetchall();

    def insertItem(self, item, tableName):
        placeholders = ', '.join(['%s'] * len(dict(item)))
        columns = ', '.join(item.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (tableName, columns, placeholders)
        self.executeSQL(sql, item.values())

    def deleteItem(self, tableName, filter):
        whereClause = self.getWhereClause(filter)
        sql = "DELETE FROM %s WHERE %s" % (tableName, whereClause)
        self.executeSQL(sql);

    def updateItem(self, item, tableName, filter):
        updates = ', '.join(['%s=%%s']* len(dict(item))) % tuple(item.keys())
        whereClause = self.getWhereClause(filter)
        sql = "UPDATE %s SET %s WHERE %s" % (tableName, updates, whereClause)
        self.executeSQL(sql, item.values())

    # filter: where条件参数，类型为字段和条件值组成的元组，如: {'field1':'"string"', 'field2':'integer'}, value需要保证类型正确，字符串字段值需要加上引号
    def getWhereClause(self, filter):
        columns = (' '.join(['%s='] * len(dict(filter))) % tuple(filter.keys())).split()  # 结果样式：[field1=, field2=, field3= ...]
        whereClause = ' AND '.join([column + '%s' for column in columns]) % tuple(filter.values())
        return whereClause

    def writeLog(self, msg, type='INFO'):
        item = SysLogItem()
        item['ProcessID'] = logid
        item['LogTime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['MsgType'] = type
        item['Message'] = msg
        self.insertItem(item, 'sys_logs')

    def __del__(self):
        self.dbcursor.close()
        self.conn.close()
        print u'数据库连接关闭，采集程序退出。'

dbhelper = DBHelper()


class DatabaseStream(logging.Handler):
    def emit(self, record):
        item = SysLogItem()
        item['ProcessID'] = logid
        item['LogTime'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        item['MsgType'] = record.levelname
        item['Message'] = record.getMessage()
        dbhelper.insertItem(item, 'sys_logs')

logger = logging.getLogger("WiBoSpider")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stdout))
logger.addHandler(DatabaseStream())
