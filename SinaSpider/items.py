# encoding=utf-8

from scrapy import Item, Field

class UserItem(Item):
    """ 个人信息 """
    Uid = Field()  # 微博发布人ID
    Uname = Field()    #昵称
    Verified = Field()  # 是否认证
    VerifiedType = Field()  # 用户认证类型
    VerifiedKind = Field()  # 用户级别
    Gender = Field()  # 性别
    GeoEnabled = Field()  # 是否开启GPS定位
    Province = Field()  # 所在省
    FollowersCount = Field()  # 被关注的数量
    FriendsCount = Field()  # 关注的好友数量
    BiFollowersCount = Field()  # 黑名单数量
    StatusesCount = Field()  # 微博数
    FavouritesCount = Field()  # 关注的微博数量

class TweetsItem(Item):
    """ 微博信息 """
    Mid = Field()  # 微博ID
    Text = Field()  # 微博内容
    Time = Field()  # 发布时间
    Uid = Field()  # 发布人
    RegPostTime = Field()    # 注册到发布此条微博的时长
    RepostCommentCount = Field()  # 回复条数
    ShareCount = Field()  # 转发条数
    AttributesCount = Field()  # 点赞数量
    Rumor = Field()  # 是否谣言
