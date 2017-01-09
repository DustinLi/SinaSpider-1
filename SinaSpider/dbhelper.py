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
        sql = self.getInsertSQL(tableName=tableName, item=item)
        self.dbcursor.execute(sql, item.values())
        self.conn.commit()

    def clearTable(self, tableName, where):
        pass

    def updateItem(self, item, tableName):
        pass

    def getInsertSQL(self, item, tableName):
        placeholders = ', '.join(['%s'] * len(dict(item)))
        columns = ', '.join(item.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (tableName, columns, placeholders)
        return sql

    def getUpdateSQL(self, item):
        pass

    def __del__(self):
        self.dbcursor.close()
        self.conn.close()