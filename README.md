# weibo-scrapy
第一，pip安装Scrapy。

第二，cmd命令行输入scrapy startproject weibo

第三，进入weibo文件夹，SHIFT加右键进入powershell输入scrapy genspider wb web

第四，打开item.py编辑，抓取微博用户id账号、微博用户名、微博内容等，（通过m.weibo.cn的api可以获取很多字段）

import scrapy
class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    _name = scrapy.Field()
    _text = scrapy.Field()
    
第五，新建get_cookie.py，用来获取cookie。

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
browser_options = Options()
browser = webdriver.Chrome(options=browser_options)
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                         '/103.0.0.0 Safari/537.36'}
print("浏览器已成功创建。")
 
 
def get_cookie(url='https://passport.weibo.cn/signin/login?'):
    url = url
    browser.get(url)
    print('现在请在Chrome浏览器中登录你的账号。')
    waiting = True
    while waiting:
        ok = input('登录成功后，输入任意内容并按回车键继续。')
        if ok:
            waiting = False
    with open('cookies.txt', 'w') as f:
        f.write(json.dumps(browser.get_cookies()))
        f.close()
    print('已成功保存cookie信息。')
 
 
if __name__ == '__main__':
    get_cookie()
（第五步没有实现）

第六，打开middlewares.py编辑，读取cookies.txt，别忘记import json。

    def process_request(self, request, spider):
        request.headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'}
        with open('cookies.txt', 'r') as f:
            cookies = json.load(f)
            request.cookies = cookies

第七，打开settings.py编辑，把以下三个的注释取掉，值改掉，其他的不用管：

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = True
ITEM_PIPELINES = {
    "weibo.pipelines.WeiboPipeline": 300,}
    
第八，打开wb.py编辑，设置spider的逻辑。

from weibo.items import WeiboItem
from copy import deepcopy
import scrapy
import json
 
class WbSpider(scrapy.Spider):
    name = "wb"
    allowed_domains = ["m.weibo.cn"]
    Q = input('请输入搜索关键词：')
    page = 1
    start_urls = [f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{Q}"
                  f"%26t%3D%26page_type=searchall&page={page}"]
 
    def parse(self, response):
        result = json.loads(response.text)
        result = result['data']['cards']
        item = WeiboItem()
        for detail in result:
            item['_id'] = detail['mblog']['user']['id']
            item['_name'] = detail['mblog']['user']['screen_name']
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++', detail['mblog']['isLongText'])
 
            if detail['mblog']['isLongText'] is True:
                blog_id = detail['mblog']['id']
                blog_id = ''.join(blog_id)
                full_text_url = 'https://m.weibo.cn/statuses/extend?id=' + blog_id
                yield scrapy.Request(full_text_url, callback=self.long_text_parse, meta={'item': deepcopy(item)},
                                     priority=1)
            else:
                _text = detail['mblog']['text']
                _text = _text.replace('\n', '')
                _text = ''.join([x.strip() for x in _text])
                item['_text'] = _text
                yield item
 
        self.page += 1
        next_page = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D{self.Q}" \
                    f"%26t%3D%26page_type=searchall&page={self.page}"
        yield scrapy.Request(next_page, callback=self.parse, meta={'item': item})
 
    def long_text_parse(self, response):
        result = json.loads(response.text)
        item = response.meta['item']
        _text = result['data']['longTextContent']
        _text = _text.replace('\n', '')
        _text = ''.join([x.strip() for x in _text])
        item['_text'] = _text
        yield item

第九，打开pipelines.py编辑，用来设置将抓取的数据导出为CSV文件。

from weibo.spiders.wb import WbSpider
import csv
class WeiboPipeline:
    def __init__(self):
        self.f = open(f'{WbSpider.Q}.csv', 'w', encoding='utf8', newline='')
        self.file_name = ['_id', '_name', '_text']
        self.writer = csv.DictWriter(self.f, fieldnames=self.file_name)
        self.writer.writeheader()
 
    def process_item(self, item, spider):
        self.writer.writerow(dict(item))
        return item
 
    def close_spider(self, spider):
        self.f.close()

第十，在cmd中启动爬虫。
cmd = e.g.'scrapy crawl wb -a keyword=王楚钦'

总结：Scrapy的难点核心在于spider文件的爬取逻辑，其他的都很easy。
————————————————
原文链接：https://blog.csdn.net/m0_72227512/article/details/131685192
