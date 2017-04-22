# -*- coding: utf-8 -*-

import scrapy

class YicheItem(scrapy.Item):
    # define the fields for your item here like:
    Date = scrapy.Field()
    CarName = scrapy.Field()
    Type = scrapy.Field()
    SalesNum = scrapy.Field()
