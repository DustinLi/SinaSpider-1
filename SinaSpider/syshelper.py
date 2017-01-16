# encoding=utf-8

from dbhelper import dbhelper, logger
from messages import system_message


class SysConfig:
    def __init__(self):
        pass

    def getAvailableSinaUser(self):
        users = dbhelper.selectItem("sina_users", {"Avaiable": "1"})
        result = None
        if len(users)>0:
            result = users[0]
        else:
            logger.error(system_message[10003])

        return result