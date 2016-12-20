# encoding=utf-8
import pymysql
import logging
from items import TweetUserItem, TweetItem


class MySQLPipleline(object):
    def __init__(self):
        self.conn = pymysql.Connect(host="localhost",
                                    user="root",
                                    password="root",
                                    db ="weibo",
                                    charset="utf8")
        self.dbcursor = self.conn.cursor()
        self.dbcursor.execute("delete from tweet_users")
        self.dbcursor.execute("delete from tweets")
        self.conn.commit()

        # self.dbcursor.execute("delete from users")
        # self.dbcursor.execute("delete from tweets")
        # self.dbcursor.close()
        # self.conn.commit()

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, TweetUserItem):
            try:
                sql = MySQLPipleline.get_sql('tweet_users', item)
                self.dbcursor.execute(sql, item.values())
                self.conn.commit();
            except Exception, e:
                logging.getLogger("mysql_pipe").error(str(e))
        elif isinstance(item, TweetItem):
            try:
                sql = MySQLPipleline.get_sql('tweets', item)
                self.dbcursor.execute(sql, item.values())
                self.conn.commit();
            except Exception, e:
                logging.getLogger("mysql_pipe").error(str(e))
        return item

    @staticmethod
    def get_sql(tableName, item):
        placeholders = ', '.join(['%s'] * len(dict(item)))
        columns = ', '.join(item.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (tableName, columns, placeholders)
        return sql

    def __del__(self):
        self.dbcursor.close()
        self.conn.close()