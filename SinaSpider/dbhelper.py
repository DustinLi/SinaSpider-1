import pymysql

class dbhelper(object):

    hostName = "localhost"
    dbUser = "root"
    dbPwd = "root"
    dbName = "weibo"
    dbCharset = "utf8"

    def __init__(self):
        self.conn = pymysql.Connect(host=self.hostName,
                                    user=self.dbUser,
                                    password=self.dbPwd,
                                    db=self.dbName,
                                    charset=self.dbCharset)
        self.dbcursor = self.conn.cursor()

    def getConnection(self):
        return self.conn

    def getCursor(self):
        return self.dbcursor

    def insertItem(self, item, tableName):
        placeholders = ', '.join(['%s'] * len(dict(item)))
        columns = ', '.join(item.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (tableName, columns, placeholders)
        self.dbcursor.execute(sql, item.values())
        self.conn.commit()

    # filter:删除记录条件参数，类型为字段和条件值组成的元组，如: {field1:value, field2:value2}
    def deleteItem(self, tableName, filter):
        columns = (' '.join(['%s='] * len(dict(filter))) % tuple(filter.keys())).split()  # 结果样式：[field1=, field2=, field3= ...]
        whereClause = ' AND '.join([column + '%s' for column in columns]) % tuple(filter.values())
        sql = "DELETE FROM %s WHERE %s" % (tableName, whereClause)
        self.dbcursor.execute(sql)
        self.conn.commit()

    def updateItem(self, item, tableName):
        pass

    def __del__(self):
        self.dbcursor.close()
        self.conn.close()