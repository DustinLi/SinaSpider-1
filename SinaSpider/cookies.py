# encoding=utf-8
import json
import base64
import requests
from syshelper import SysConfig

config = SysConfig()
user = config.getAvailableSinaUser()
if user is not None:
    name = user[0]
    pwd = user[1]
else:
    exit()


def getCookies(uname, password):
    """ 获取Cookies """
    cookies = []
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'

    username = base64.b64encode(uname.encode('utf-8')).decode('utf-8')
    postData = {
        "entry": "sso",
        "gateway": "1",
        "from": "null",
        "savestate": "30",
        "useticket": "0",
        "pagerefer": "",
        "vsnf": "1",
        "su": username,
        "service": "sso",
        "sp": password,
        "sr": "1440*900",
        "encoding": "UTF-8",
        "cdult": "3",
        "domain": "sina.com.cn",
        "prelt": "0",
        "returntype": "TEXT",
    }
    session = requests.Session()
    r = session.post(loginURL, data=postData)
    jsonStr = r.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print u"Cookie获取成功!( 账号: %s )" % uname
        cookie = session.cookies.get_dict()
        cookies.append(cookie)
    else:
        print u"获取Cookie失败！( 原因:%s )" % info['reason']
    return cookies


cookies = getCookies(name, pwd)
print u"Cookie获取完成!( 编号: %d)" % len(cookies)
