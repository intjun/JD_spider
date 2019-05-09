# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from JD_spider.items import JdSpiderItem
import pymongo

class JdSpiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item ,JdSpiderItem):
            if item.get('comment_num')and item.get('good_count'):
                item['good_rate_show'] = ('%.2f%%' % (float(item.get('good_count'))*100/float(item.get('comment_num'))))
        return item

class MongoPipeline(object):

    table_name = '车'
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db =crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #print(item.get('id'))
        self.db[self.table_name].update({'url':item.get('url')},{'$set':dict(item)},True)
        return item

