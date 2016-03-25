# -*- coding: utf-8 -*-
import scrapy
from sjgtw_links.items import SjgtwLinksItem
import time
import json
import codecs
from scrapy import log


class linkSpider(scrapy.Spider):
    name = 'sjgtw_links'
    allow_domains = ["sjgtw.com"]
    # start_urls = ['']
    start_urls = ['http://www.sjgtw.com/goodsClass/goodsClassIndex?clickId=1'] # test
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "clientId=38681443894000; clientId=38681446210000; JSESSIONID=372570A67852F5343A0E9C01BA4F5F6D; Hm_lvt_8908fa41684e227cc7f033849052cd8a=1458723279; Hm_lpvt_8908fa41684e227cc7f033849052cd8a=1458723806; CNZZDATA1256025023=1839444177-1458720018-%7C1458720018"
    }

    def __init__(self):

        self.file = codecs.open('links.txt', 'a')  # append mode
        self.file.write("level\tname\tclickId\turl\tfrom_url\n")
        self.urls_seen = set()
        self.urls_crawled = set()
        for i in range(1, 7000):  # max: 6947
            self.start_urls.append("http://www.sjgtw.com/goodsClass/goodsClassIndex?clickId=%d" % i)
            # crawled = open("crawled.txt", 'r')
            # while 1:
            #     line = crawled.readline()
            #     if not line:
            #         break
            #     self.urls_crawled.add(line.split('\t')[4])  # requesed pages
            #     self.urls_seen.add(line.split('\t')[3])  # saved items
            #
            # print(">>>> %d crawled links loaded. " % len(self.urls_crawled))
        super(linkSpider, self).__init__()

    def parse(self, response):

        if response.body.find("FreeMarker template error:") > 0:
            log.INFO("invalid page %s " % response.url)
            return
        nodeXpath = "//a[@class='_blue' and contains(@href,'%s')]" % response.url[response.url.find("clickId="):]
        node = response.xpath(nodeXpath)
        if len(node) == 0:
            log.err("item not found. %s " % response.url)
        item = SjgtwLinksItem()
        item['name'] = node.xpath("./text()")[0].extract().encode("utf-8")
        item['level'] = node.xpath("./../../span[@class='ladder']/text()")[0].extract().encode("utf-8")
        item['url'] = response.url
        item['clickId'] = int(response.url[response.url.find("clickId=") + 8:])
        # parent
        parentXpath = "((//a[@class='_blue' and contains(@href,'%s')]/../..)[@class='row']/preceding::div[@class='row']//a[@class='_blue'])[last()]" % response.url[response.url.find("clickId="):]
        parent = response.xpath(parentXpath)
        if len(parent) > 0:
            parentHref = parent.xpath("./@href")[0].extract()
            # [parent.xpath("./@href")[0].extract().find("clickId=")+8:]
            item['parentClickId'] = int(parentHref[parentHref.find("clickId=") + 8:])
        yield item

        # ((//a[@class='_blue' and contains(@href,'clickId=6945')]/../..)[@class='row']/preceding::div[@class='row']//a[@class='_blue'])[last()] # 父节点
        # print(node.extract())
