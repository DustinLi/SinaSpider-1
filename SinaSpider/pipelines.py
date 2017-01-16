# encoding=utf-8

from dbhelper import dbhelper, logger
from items import TweetUserItem, TweetItem


class MySQLPipleline(object):
    def __init__(self):
        self.conn = dbhelper.conn
        self.dbcursor = dbhelper.dbcursor

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, TweetUserItem):
            try:
                dbhelper.insertItem(item, 'tweet_users')
            except Exception, e:
                logger.error(str(e))
        elif isinstance(item, TweetItem):
            try:
                dbhelper.insertItem(item, 'tweets')
            except Exception, e:
                logger.error(str(e))
        return item