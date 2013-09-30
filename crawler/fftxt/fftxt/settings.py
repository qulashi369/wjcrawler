# Scrapy settings for fftxt project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'fftxt'

SPIDER_MODULES = ['fftxt.spiders']
NEWSPIDER_MODULE = 'fftxt.spiders'

ITEM_PIPELINES = [
    'fftxt.pipelines.FftxtPipeline',
]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'fftxt (+http://www.yourdomain.com)'
