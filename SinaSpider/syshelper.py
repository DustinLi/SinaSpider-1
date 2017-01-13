# encoding=utf-8

from dbhelper import dbhelper, logger

class SysConfig:

    def getAvailableSinaUser(self):
        users = dbhelper.selectItem("sina_users", {"Avaiable": "1"})
        result = None
        if len(users)>0:
            result = users[0]
        else:
            logger.info(u'没有可用的新浪微博用户，请添加微博用户账号')

        return result