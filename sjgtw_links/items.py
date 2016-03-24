# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SjgtwLinksItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    level = scrapy.Field()
    url = scrapy.Field()
    from_url = scrapy.Field()
    clickId = scrapy.Field()
    insert_time = scrapy.Field()
    pass
