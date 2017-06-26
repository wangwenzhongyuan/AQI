# -*- coding: utf-8 -*-

from scrapy.exporters import CsvItemExporter
import json
from redis import Redis
import pymongo

from datetime import datetime

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class UtcPipeline(object):
    def process_item(self, item, spider):
        #utcnow() 是获取UTC时间
        item["crawled"] = datetime.utcnow()
        # 爬虫名
        # item["spider"] = spider.name
        return item

class SaqiPipeline(object):
    #写入csv
    def open_spider(self, spider):
        #创建csv文件
        self.csvFile = open('saqi.csv', 'w')
        #创建读写对象
        self.csvExporter = CsvItemExporter(self.csvFile)
        #可以开始进行写入
        self.csvExporter.start_exporting()
    def process_item(self, item, spider):
        #写入对象
        self.csvExporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.csvExporter.finish_exporting()
        self.csvFile.close()
#存入有redis中
class SaqiRedisPipeline(object):
    def open_spider(self, spider):
        #创建数据库链接对象
        self.redis_cli = Redis(host='192.168.154.129', port=6379)

    def process_item(self, item, spider):
        #将item转换成json格式,item只有scrapy模块认识(存为何中格式，看需求)
        content = json.dumps(dict(item), ensure_ascii=False)
        #按照列表存入redis中
        self.redis_cli.lpush('AQI', content)
        return item

class SaqiMongoPipeline(object):
    def open_spider(self, spider):
        #创建链接对象
        self.mongo_cli = pymongo.MongoClient(host='192.168.154.129', port=27017)
        #创建数据库
        self.dbname = self.mongo_cli['AQI']
        #创建表
        self.sheet = self.dbname['AQI_DATA']
        #mongodb可以直接存python的字典

    def process_item(self, item, spider):
        self.sheet.insert(dict(item))
        return item



