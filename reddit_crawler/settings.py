# -*- coding: utf-8 -*-

BOT_NAME = 'reddit_crawler'

SPIDER_MODULES = ['reddit_crawler.spiders']
NEWSPIDER_MODULE = 'reddit_crawler.spiders'

DEPTH_LIMIT = 0
DOWNLOAD_DELAY = 1

ITEM_PIPELINES = {'reddit_crawler.pipelines.JsonExportPipeline': 300, }


FEED_URI = 'file:///tmp/export.json'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'reddit_crawler (+http://www.yourdomain.com)'
