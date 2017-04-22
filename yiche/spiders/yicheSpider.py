# -*- coding:utf-8 -*-

import scrapy
from scrapy.http import Request
from yiche.items import YicheItem
import re

# create UrlList

T = ['jincouxingche','xiaoxingche','weixingche','zhongxingche','zhongdaxingche','suv','mpv']


class YicheSpider(scrapy.spiders.Spider):
    name = "yiche"
    allowed_domains = ["index.bitauto.com"]

    start_urls = ['http://index.bitauto.com/xiaoliang/%s/%sm%s/1'%(t,y,m) for t in T for y in range(2010,2017) for m in range(1,13)]

    def parse(self, response):

        # 获取第一个页面的数据
        s = response.url
        t,year,m = re.findall('xiaoliang/(.*?)/(\d+)m(\d+)',s,re.S)[0]

        for sel in response.xpath('//ol/li'):

            Name = sel.xpath('a/text()').extract()[0]
            SalesNum = sel.xpath('span/text()').extract()[0]
            #print(Name,SalesNum)
            items = YicheItem()
            items['Date'] = str(year)+'/'+str(m)
            items['CarName'] = Name
            items['Type'] = t
            items['SalesNum'] = SalesNum
            yield items


        # 判断是否还有下一页，如果没有跳过，有则爬取下一个页面
        if len(response.xpath('//div[@class="the_pages"]/@class').extract())==0:
            pass
        else:
            next_pageclass = response.xpath('//div[@class="the_pages"]/div/span[@class="next_off"]/@class').extract()
            next_page = response.xpath('//div[@class="the_pages"]/div/span[@class="next_off"]/text()').extract()

            if len(next_page)!=0 and len(next_pageclass)!=0:
                pass
            else:
                next_url = 'http://index.bitauto.com'+response.xpath('//div[@class="the_pages"]/div/a/@href')[-1].extract()
                yield Request(next_url, callback=self.parse)
