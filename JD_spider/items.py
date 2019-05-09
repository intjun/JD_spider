# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item ,Field

class JdSpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = Field()
    file_path = Field()
    price = Field()
    comment_num = Field()
    good_count = Field()
    good_rate_show = Field()
    url = Field()