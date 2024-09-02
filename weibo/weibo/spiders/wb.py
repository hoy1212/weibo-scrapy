from datetime import datetime
import random
from weibo.items import WeiboItem
from copy import deepcopy
import scrapy
import json


class WbSpider(scrapy.Spider):
    name = "wb"
    allowed_domains = ["m.weibo.cn"]

    def __init__(self, keyword=None, *args, **kwargs):
        super(WbSpider, self).__init__(*args, **kwargs)
        self.keyword = keyword
        self.page = 1
        self.max_pages = 200
        # 更新start_urls以使用命令行中传入的关键词
        # self.start_urls = [f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{self.keyword}%26t%3D%26page_type=searchall&page={self.page}"]#实时
        # self.start_urls = [f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{self.keyword}%26t%3D%26page_type=searchall&page={self.page}"] #综合
        self.start_urls = [f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D{self.keyword}%26t%3D%26page_type=searchall&page={self.page}"] #热门

    def set_user_agent(self, request):
        user_agent = random.choice(self.settings.get('USER_AGENT_LIST'))
        request.headers['User-Agent'] = user_agent
        return request

    def parse(self, response):
        if self.page > self.max_pages:
            return
        result = json.loads(response.text)
        page_data = result.get('data', {})
        cards = page_data.get('cards', [])

        for card in cards:
            if card.get('card_type') == 9:  # We focus on card_type 9 for weibo posts
                yield from self.extract_item(card)

        self.page += 1
        # next_page = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{self.keyword}%26t%3D%26page_type=searchall&page={self.page}"#实时
        # next_page = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{self.keyword}%26t%3D%26page_type=searchall&page={self.page}"#综合
        next_page = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D{self.keyword}%26t%3D%26page_type=searchall&page={self.page}"#hot
        yield scrapy.Request(next_page, callback=self.parse)

    def extract_item(self, card):
        mblog = card.get('mblog', {})
        user = mblog.get('user', {})
        item = WeiboItem()
        item['_id'] = user.get('id', '')
        item['_name'] = user.get('screen_name', '')
        item['_region'] = mblog.get('region_name', 'Unknown')

        # Additionally extract followers_count, reposts_count, comments_count, and attitudes_count
        item['_followers'] = user.get('followers_count', '0')  # User followers count
        item['_reposts'] = mblog.get('reposts_count', 0)  # Number of reposts for the post
        item['_comments'] = mblog.get('comments_count', 0)  # Number of comments for the post
        item['_likes'] = mblog.get('attitudes_count', 0)  # Number of likes for the post

        created_at = mblog.get('created_at', '')
        if created_at:
            parsed_date = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
            item['_time'] = parsed_date.strftime("%d/%m/%Y")

        if mblog.get('isLongText', False):
            blog_id = mblog.get('id', '')
            full_text_url = f"https://m.weibo.cn/statuses/extend?id={blog_id}"
            yield scrapy.Request(full_text_url, callback=self.long_text_parse, meta={'item': deepcopy(item)}, priority=1)
        else:
            text = mblog.get('text', '').replace('\n', '').strip()
            item['_text'] = text
            yield item

    def long_text_parse(self, response):
        result = json.loads(response.text)
        item = response.meta['item']
        _text = result['data']['longTextContent']
        _text = _text.replace('\n', '')
        _text = ''.join([x.strip() for x in _text])
        item['_text'] = _text
        yield item
