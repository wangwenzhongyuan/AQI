# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from SAQI.items import SaqiItem

#0:到如类
from scrapy_redis.spiders import RedisSpider

#１　修改继承的类
class SaqiSpider(RedisSpider):
    name = 'saqi'
    # allowed_domains = ['aqistudy.cn']
    # start_urls = ['https://www.aqistudy.cn/historydata/']
    # start_urls = ['https://www.aqistudy.cn/historydata/']
    #类名的小写加上start_urls表示从master断的数据库里起始url的建，表示获取
    
    redis_key = 'saqispider:start_urls'

    #follow = True表示继续跟进，即第一批的处理完了，接着继续提取接下来的链接,重复的链接不入队列
    #为true每个响应文件都会经过这里。｛Rule发请求，LinkExtractor(链接提取器)提取链接，｝
    #follow表示是否继续跟进新的链接，如果false表示拿到响应之后就不在提取链接了

    rules = [Rule(LinkExtractor(allow=r'https://www.aqistudy.cn/historydata/monthdata.php\?city=\.*'), follow=True),
        Rule(LinkExtractor(allow=r'&month=\.*'), callback='parse_day', follow=True)]
#上面，如果没有指定回调函数，ｆｏｌｌｏｗ默认为True,

    # def parse_month(self, response):
        #响应文件有两个工作，一是到达指定的解析函数去提取数据，二是提取新的链接，LinkExtractor得到新的链接，继续发请求给调度器。因为在当前页面提取到链接了，就不用yield　scarpy.Request()发送请求了。spider只是提取数据
        # i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i

    def parse_day(self, response):

        # print response.body
        day_list = response.xpath('//table[@class="table table-condensed table-bordered table-striped table-hover table-responsive"]//tr')

        day_list.pop(0)
        for day in day_list:
            item = SaqiItem()
            city_name = response.xpath('//h2[@id="title"]/text()').extract()[0][8:-11]
            # print city_name
            
            item['city'] = city_name.encode('utf-8')
            item['date'] = day.xpath('./td[1]/text()').extract()[0].encode('utf-8')
            item['aqi'] = day.xpath('./td[2]/text()').extract()[0].encode('utf-8')
            item['level'] = day.xpath('./td[3]/div/text()').extract()[0].encode('utf-8')
            item['pm2_5'] = day.xpath('./td[4]/text()').extract()[0].encode('utf-8')
            item['pm10'] = day.xpath('./td[5]/text()').extract()[0].encode('utf-8')
            item['so2'] = day.xpath('./td[6]/text()').extract()[0].encode('utf-8')
            item['co'] = day.xpath('./td[7]/text()').extract()[0].encode('utf-8')
            item['no2'] = day.xpath('./td[8]/text()').extract()[0].encode('utf-8')
            item['o3'] = day.xpath('./td[9]/text()').extract()[0].encode('utf-8')
            item['rank'] = day.xpath('./td[10]/text()').extract()[0].encode('utf-8')
            yield item

        # for day in day_list:
        #     print day
        # print day_list
