# -*- coding: utf-8 -*-
import scrapy
from sjgtw_links.items import SjgtwLinksItem
import time
import json
import codecs


class linkSpider(scrapy.Spider):
    name = 'sjgtw_links'
    allow_domains = ["sjgtw.com"]
    start_urls = ['http://www.sjgtw.com/goodsClass/goodsClassIndex?clickId=1']
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "clientId=38681443894000; clientId=38681446210000; JSESSIONID=372570A67852F5343A0E9C01BA4F5F6D; Hm_lvt_8908fa41684e227cc7f033849052cd8a=1458723279; Hm_lpvt_8908fa41684e227cc7f033849052cd8a=1458723806; CNZZDATA1256025023=1839444177-1458720018-%7C1458720018"
    }

    def __init__(self):
        super(linkSpider, self).__init__()
        self.file = codecs.open('links.txt', 'w')
        self.file.write("level\tname\tclickId\turl\tfrom_url\n")
        self.urls_seen = set()
        self.urls_crawled = set()

        crawled = open("crawled.txt", 'r')
        while 1:
            line = crawled.readline()
            if not line:
                break
            self.urls_crawled.add(line)

        print(">>>> %d crawled links loaded. " % len(self.urls_crawled))

    def parse(self, response):
        catalogys = response.xpath("//div[@class='row']/span[@class='catalogy_span']")
        print("found %d links from %s" % (len(catalogys), response.url))
        for catalogy in catalogys:  # a[@href, 'goodsClass']

            item = SjgtwLinksItem()
            item['name'] = catalogy.xpath("./a/text()")[0].extract().encode("utf-8")

            item['level'] = catalogy.xpath("./../span[@class='ladder']/text()")[0].extract().encode("utf-8")
            item['url'] = "http://www.sjgtw.com%s" % (catalogy.xpath("./a/@href")[0].extract().encode("utf-8"))
            item['from_url'] = response.url

            if item['url'].find("clickId=") > -1:
                item['clickId'] = int(item['url'][item['url'].find("clickId=") + 8:])
            # item['insert_time'] = time.asctime(time.localtime(time.time()))
            # yield item

            href = item['url']
            # print(href)
            if not item['url'] in self.urls_seen:
                # line = json.dumps(dict(item))

                line = item['level'] + "\t" + item['name'] + "\t" + str(item['clickId']) + "\t" + item['url'] + "\t" + item['from_url']

                self.file.write(line + "\n")
                print(line)
                self.urls_seen.add(item['url'])
            else:
                print("url seen %s" % href)
            if href not in self.urls_crawled:  # 已经爬过的的页面不再爬取
                print("crawling %s from %s " % (href, response.url))
                yield scrapy.Request(href, callback=self.parse)
            else:
                print("url %s crawled before... pass" % href)
        self.urls_crawled.add(response.url)
        print("url %s added to urls_crawled." % response.url)
