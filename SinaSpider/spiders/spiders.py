# encoding=utf-8
import re

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from SinaSpider.items import TweetUserItem, TweetItem


class Spider(CrawlSpider):
    name = "sinaSpider"
    host = "http://weibo.cn"

    user_ids = [
        # u'2954342027' http://weibo.cn/2954342027/follow
        # 1829429022
    ]
    scrawl_ID = set(user_ids)  # 记录待爬的微博ID
    finish_ID = set()  # 记录已爬的微博ID

    def start_requests(self):
        yield Request(url=self.host, callback=self.parse_login_user)
        # while True:
        #     if self.scrawl_ID:
        #         user_id = self.scrawl_ID.pop()
        #         if user_id:
        #             self.finish_ID.add(user_id)  # 加入已爬队列
        #             user_id = str(user_id)
        #             url_user = "http://weibo.cn/u/%s?filter=1" % user_id
        #             yield Request(url=url_user, meta={"user_id": user_id}, callback=self.parse_user)  # 去爬用户
        #             url_tweet = "http://weibo.cn/%s/profile?filter=0&page=230" % user_id
        #             yield Request(url=url_tweet, meta={"user_id": user_id}, callback=self.parse_tweets)
        #         else:
        #             break
        #     else:
        #         break

    # start_urls = ['http://weibo.cn/1829429022/profile?filter=0&page=230']
    #
    # def parse(self, response):
    #     page = response.xpath(u"//a[text()='下页']/@href").extract_first()
    #     # print "########### " + page + " #################"
    #     #text = response.css(".ctt").xpath(u"./text()[contains(., '太活跃的鱼千万别买')]").extract_first()
    #     #text = response.css(".ctt").xpath(u"./text()[contains(., '太活跃的鱼千万别买')]").extract_first()
    #     rumor = response.xpath("//span[@class='kt']/text()").extract_first()
    #     # text1 = response.css(".ctt").xpath(u"./text()").extract_first()
    #     # print text1;
    #     if rumor is not None:
    #         print "----------------------------- " + page + " ------------------------------"
    #         print "-----------------------------" + rumor[1:9] + "---------------------------"
    #     else:
    #         next_url = response.urljoin(page)
    #         print "#################" + next_url + "################"
    #         yield scrapy.Request(next_url, self.parse)

    #解析登录用户关注的用户，开始循环无尽爬取用户
    def parse_login_user(self, response):
        selector = Selector(response)
        path = selector.xpath(u'//a[text()="\u8be6\u7ec6\u8d44\u6599"]/@href').extract_first()
        if (path is not None) and (path != ""):
            uid=re.findall(u'/(\d*)/.*', path)
            if (len(uid) > 0) and (uid[0] != ''):
                url_follow = 'http://weibo.cn/%s/follow' % uid[0]
                yield Request(url=url_follow, callback=self.parse_follower)

    # 爬取当前登录用户关注的用户，只爬第一页
    def parse_follower(self, respose):
        selector = Selector(respose)
        url_followers = selector.xpath('/html/body/table[*]/tr/td[1]/a/@href').extract()
        for url_follower in url_followers:
            yield Request(url=url_follower, callback=self.parse_follow_user)
        else:
            #follow用户完成后挑选follower中的用户作为宿主查找此用户的followers
            if len(self.user_ids) > 0:
                url_next = 'http://weibo.cn/%s/follow' % self.user_ids.pop(0)
                yield Request(url=url_next, callback=self.parse_follower)


    # 爬取用户ID数据
    def parse_follow_user(self, response):
        selector = Selector(response)
        path = selector.xpath(u'//a[text()="\u8d44\u6599"]/@href').extract_first()
        if (path is not None) and (path != ""):
            uid = re.findall(u'/(\d*)/.*', path)
            if (len(uid) > 0) and (uid[0] != ''):
                self.user_ids.append(uid[0])         #记录所有用户ID，为爬取其followers的数据
                url_user = "http://weibo.cn/u/%s?filter=1" % uid[0]
                yield Request(url=url_user, meta={"user_id": uid[0]}, callback=self.parse_user)  # 去爬用户
                url_tweet = "http://weibo.cn/%s/profile?filter=0" % uid[0]
                yield Request(url=url_tweet, meta={"user_id": uid[0]}, callback=self.parse_tweets)

    def parse_user(self, response):
        """ 抓取个人信息1 """
        userItem = TweetUserItem()
        selector = Selector(response)
        verifiedAll = selector.xpath('body/div[@class="u"]/table//div[@class="ut"]')
        verifiedSelector = verifiedAll.xpath('//img[@alt="V"]')
        verifiedType = None
        if verifiedSelector:
            userItem["Verified"] = True                                        # 是否认证
            userItem["VerifiedType"] = verifiedAll.xpath(u'//span[contains(text(), "认证")]/text()').extract_first()          # 认证类型
        else:
            userItem["Verified"] = False
            userItem["VerifiedType"] = "N/A"

        allTips = selector.xpath('body/div[@class="u"]/div[@class="tip2"]').extract_first()
        if allTips:
            statusesCount = re.findall(u'\u5fae\u535a\[(\d+)\]', allTips)  # 微博数
            friendsCount = re.findall(u'\u5173\u6ce8\[(\d+)\]', allTips)  # 关注的微博（好友）数
            followersCount = re.findall(u'\u7c89\u4e1d\[(\d+)\]', allTips)  # 粉丝数
            if statusesCount:
                userItem["StatusesCount"] = int(statusesCount[0])
            if friendsCount:
                userItem["FriendsCount"] = int(friendsCount[0])                 # 关注的好友
                userItem["FavouritesCount"] = int(friendsCount[0])              # 关注的微博
            if followersCount:
                userItem["FollowersCount"] = int(followersCount[0])
            userItem["Uid"] = response.meta["user_id"]
            url_user_detail = "http://weibo.cn/%s/info" % response.meta["user_id"]
            yield Request(url=url_user_detail, meta={"item": userItem}, callback=self.parse_user_detail)

    def parse_user_detail(self, response):
        """ 抓取个人信息2 """
        userItem = response.meta["item"]
        selector = Selector(response)
        allTipsDetail = ";".join(set(selector.xpath('body/div[@class="c"]/text()').extract()))  # 获取标签里的所有text()

        nickname = re.findall(u'\u6635\u79f0[:|\uff1a](.*?);', allTipsDetail)  # 昵称
        gender = re.findall(u'\u6027\u522b[:|\uff1a](.*?);', allTipsDetail)    # 性别
        province = re.findall(u'\u5730\u533a[:|\uff1a](.*?);', allTipsDetail)  # 地区（包括省份和城市）
        verifiedKind = re.findall(u'\u4f1a\u5458\u7b49\u7ea7[:|\uff1a](.*?)\u7ea7[\s;]*', allTipsDetail)        # 用户级别

        # birthday = re.findall(u'\u751f\u65e5[:|\uff1a](.*?);', text1)  # 生日
        # sexorientation = re.findall(u'\u6027\u53d6\u5411[:|\uff1a](.*?);', text1)  # 性取向
        # marriage = re.findall(u'\u611f\u60c5\u72b6\u51b5[:|\uff1a](.*?);', text1)  # 婚姻状况
        # signature = re.findall(u'\u7b80\u4ecb[:|\uff1a](.*?);', text1)  # 个性签名
        # url = re.findall(u'\u4e92\u8054\u7f51[:|\uff1a](.*?);', text1)  # 首页链接
        if nickname:
            userItem["Uname"] = nickname[0]
        if gender:
            userItem["Gender"] = gender[0]
        if province:
            province = province[0].split(" ")
            userItem["Province"] = province[0]
        if verifiedKind:
            userItem["VerifiedKind"] = verifiedKind[0]

        userItem["GeoEnabled"] = False                              # 两个无法获取的值，暂给默认值
        userItem["BiFollowersCount"] = 0

        yield userItem

    def parse_tweets(self, response):
        """ 抓取微博数据 """
        # RegPostTime = Field()  # 注册到发布此条微博的时长
        selector = Selector(response)
        tweets = selector.xpath('body/div[@class="c" and @id]')
        for tweet in tweets:
            tweetsItems = TweetItem()
            id = tweet.xpath('@id').extract_first()  # 微博ID
            content = tweet.xpath('div/span[@class="ctt"]/text()').extract_first()  # 微博内容
            rumor = tweet.xpath('div/span[@class="kt"]')            # 谣言
            # cooridinates = tweet.xpath('div/a/@href').extract_first()  # 定位坐标
            attributesCount = re.findall(u'\u8d5e\[(\d+)\]', tweet.extract())  # 点赞数
            shareCount = re.findall(u'\u8f6c\u53d1\[(\d+)\]', tweet.extract())  # 转载数
            comment = re.findall(u'\u8bc4\u8bba\[(\d+)\]', tweet.extract())  # 评论数
            others = tweet.xpath('div/span[@class="ct"]/text()').extract_first()   # 求时间和使用工具（手机或平台）

            tweetsItems["Mid"] = id
            tweetsItems["Uid"] = response.meta["user_id"]
            if content:
                tweetsItems["Text"] = content.strip(u"[\u4f4d\u7f6e]")  # 去掉最后的"[位置]"
            # if cooridinates:                                             # 开户地理位置信息
            #     cooridinates = re.findall('center=([\d|.|,]+)', cooridinates)
            #     if cooridinates:
            #         tweetsItems["Co_oridinates"] = cooridinates[0]
            if attributesCount:
                tweetsItems["AttributesCount"] = int(attributesCount[0])          # 点赞数
            if shareCount:
                tweetsItems["ShareCount"] = int(shareCount[0])            # 转载数
            if comment:
                tweetsItems["RepostCommentCount"] = int(comment[0])          # 评论数
            if others:
                others = others.split(u"\u6765\u81ea")
                tweetsItems["Time"] = others[0]                                 # 发表时间
                # if len(others) == 2:                                           # 使用的工具/手机
                #     tweetsItems["Tools"] = others[1]
            if rumor:
                tweetsItems["Rumor"] = True
            else:
                tweetsItems["Rumor"] = False
            yield tweetsItems
        url_next = selector.xpath(
            u'body/div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], meta={"user_id": response.meta["user_id"]}, callback=self.parse_tweets)

    def parse3(self, response):
        """ 抓取关注或粉丝 """
        items = response.meta["item"]
        selector = Selector(response)
        text2 = selector.xpath(
            u'body//table/tr/td/a[text()="\u5173\u6ce8\u4ed6" or text()="\u5173\u6ce8\u5979"]/@href').extract()
        for elem in text2:
            elem = re.findall('uid=(\d+)', elem)
            if elem:
                response.meta["result"].append(elem[0])
                ID = int(elem[0])
                if ID not in self.finish_ID:  # 新的ID，如果未爬则加入待爬队列
                    self.scrawl_ID.add(ID)
        url_next = selector.xpath(
            u'body//div[@class="pa" and @id="pagelist"]/form/div/a[text()="\u4e0b\u9875"]/@href').extract()
        if url_next:
            yield Request(url=self.host + url_next[0], meta={"item": items, "result": response.meta["result"]},
                          callback=self.parse3)
        else:  # 如果没有下一页即获取完毕
            yield items
