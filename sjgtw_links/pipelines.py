# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo

from scrapy.conf import settings
from scrapy import log
from scrapy.exceptions import DropItem


class SjgtwLinksPipeline(object):
    def __init__(self):

        self.urls_seen = set()

        # connection = pymongo.MongoClient("mongodb://"+settings['MONGODB_SERVER']+":"+str(settings['MONGODB_PORT']))
        # db = connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]
        connection = pymongo.MongoClient("mongodb://guanxiaoda.cn:27017")
        db = connection[settings['MONGODB_DB']]

        self.collection = db[settings['MONGODB_COLLECTION']]
        log.msg(">>>loading items crawled before...")
        items = self.collection.find()
        for item in items:
            self.urls_seen.add(item['url'])
        log.msg(">>>load %d seen urls from mongodb" % len(self.urls_seen))
        # db = connection['housedb']
        # self.collection = db['houseinfo']

    def process_item(self, item, spider):
        valid = True
        # for data in item:
        # here we only check if the data is not null
        # but we could do any crazy validation we want
        if not item['clickId']:
            valid = False
            raise DropItem("Missing clickId %s" % item)
        if item['url'] in self.urls_seen:  # crawled before
            valid = False
            raise DropItem("item %s already in mongodb." % item)
        if valid:
            self.urls_seen.add(item['url'])
            self.collection.insert(dict(item))
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
        return item
