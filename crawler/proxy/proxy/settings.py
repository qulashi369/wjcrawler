# Scrapy settings for proxy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'proxy'

SPIDER_MODULES = ['proxy.spiders']
NEWSPIDER_MODULE = 'proxy.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'

DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 30

ITEM_PIPELINES = [ 'proxy.pipelines.ProxyPipeline' ]

