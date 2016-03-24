# -*- coding: utf-8 -*-

# Scrapy settings for sjgtw_links project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
DOWNLOAD_DELAY = 5

BOT_NAME = 'sjgtw_links'

SPIDER_MODULES = ['sjgtw_links.spiders']
NEWSPIDER_MODULE = 'sjgtw_links.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sjgtw_links (+http://www.yourdomain.com)'
