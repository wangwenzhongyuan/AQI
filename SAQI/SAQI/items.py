# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SaqiItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    date = scrapy.Field()
    aqi = scrapy.Field()
    level = scrapy.Field()
    pm2_5 = scrapy.Field()
    pm10 = scrapy.Field()
    so2 = scrapy.Field()
    co = scrapy.Field()
    no2 = scrapy.Field()
    o3 = scrapy.Field()
    rank = scrapy.Field()
    #存放爬虫名字的字段
    spider = scrapy.Field()
    crawler = scrapy.Field()
