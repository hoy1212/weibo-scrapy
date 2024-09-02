# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from weibo.spiders.wb import WbSpider
from itemadapter import ItemAdapter
import csv
import re  # 导入正则表达式库


class WeiboPipeline:
    def __init__(self):
        self.file_name = None  # 不再在初始化时设置文件名
        self.file = None
        self.writer = None

    def open_spider(self, spider):
        # 从spider实例获取keyword
        keyword = getattr(spider, 'keyword', 'default_keyword')
        self.file_name = f'{keyword}.csv'
        self.file = open(self.file_name, 'w', encoding='utf8', newline='')
        field_names = ['_id', '_name', '_region', '_time', '_text', '_followers', '_reposts', '_comments','_likes']  # 确保这些与item字段匹配
        self.writer = csv.DictWriter(self.file, fieldnames=field_names)
        self.writer.writeheader()

    def process_item(self, item, spider):
        # 使用ItemAdapter来兼容不同的item类型
        adapter = ItemAdapter(item)
        if adapter.get('_text'):
            adapter['_text'] = self.clean_text(adapter['_text'])  # 清理_text字段
        self.writer.writerow({field: adapter.get(field) for field in self.writer.fieldnames})
        return item

    def clean_text(self, text):
        # 移除<a>标签及其内容
        text = re.sub(r'<a[^>]*>(.*?)</a>', '', text)
        # 移除剩余的HTML标签
        text = re.sub(r'<[^>]*>', '', text)
        # 移除额外的空格和转义字符
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def close_spider(self, spider):
        self.file.close()
