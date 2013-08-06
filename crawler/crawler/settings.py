#-*- coding: utf-8 -*-
# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
ITEM_PIPELINES = ['crawler.pipelines.CrawlerPipeline']

#DEPTH_PRIORITY = 1
#SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
#SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler (+http://www.yourdomain.com)'
