#-*- coding: utf-8 -*-

import os

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
ITEM_PIPELINES = ['crawler.pipelines.ContentPipeline']

DOWNLOAD_DELAY = 1.5  # 0.5*1.5 - 1.5*1.5 s
DOWNLOAD_TIMEOUT = 20  # 60s
COOKIES_ENABLED = False
CONCURRENT_REQUESTS_PER_DOMAIN = 5

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_AGENTS_LIST_FILE = os.path.join(project_dir, 'user-agents.txt')
#PROXY_LIST_FILE = os.path.join(project_dir, 'proxies.txt')

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Proxy-Connection': 'keep-alive'
}


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'crawler.middleware.UserAgentsMiddleware': 400,
    #'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    #'crawler.middleware.ProxyMiddleware': 100,
}
