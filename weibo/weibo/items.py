# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class RedbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    笔记标题 = scrapy.Field()
    笔记链接 = scrapy.Field()
    用户ID = scrapy.Field()
    用户名 = scrapy.Field()
    头像链接 = scrapy.Field()
    IP属地 = scrapy.Field()
    笔记发布时间 = scrapy.Field()
    笔记收藏数 = scrapy.Field()
    笔记评论数 = scrapy.Field()
    笔记点赞数 = scrapy.Field()
    笔记转发数 = scrapy.Field()
    笔记内容 = scrapy.Field()


class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    _name = scrapy.Field()
    _region = scrapy.Field()
    _time = scrapy.Field()
    _text = scrapy.Field()
    _followers = scrapy.Field()
    _reposts = scrapy.Field()
    _comments = scrapy.Field()
    _likes = scrapy.Field()
