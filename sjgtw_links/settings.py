# -*- coding: utf-8 -*-

# Scrapy settings for sjgtw_links project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
DOWNLOAD_DELAY = 3

BOT_NAME = 'sjgtw_links'

SPIDER_MODULES = ['sjgtw_links.spiders']
NEWSPIDER_MODULE = 'sjgtw_links.spiders'


MONGODB_DB = 'sjgtwdb'
MONGODB_COLLECTION = 'sjgtw_catalog'

ITEM_PIPELINES={
    # 'Lianjia.pipelines.pipelines.LianjiaJsonPipeline':300,
    'sjgtw_links.pipelines.SjgtwLinksPipeline':800
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sjgtw_links (+http://www.yourdomain.com)'
