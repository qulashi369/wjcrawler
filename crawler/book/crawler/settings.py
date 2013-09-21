#-*- coding: utf-8 -*-

import os

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
ITEM_PIPELINES = ['crawler.pipelines.MyImagePipeline',
                  'crawler.pipelines.BookPipeline',
                  'crawler.pipelines.ChapterPipeline',
                  'crawler.pipelines.ContentPipeline']

#ITEM_PIPELINES = ['crawler.pipelines.MyImagePipeline', 'crawler.pipelines.BookPipeline']
#ITEM_PIPELINES = ['crawler.pipelines.ChapterPipeline']
#ITEM_PIPELINES = ['crawler.pipelines.ContentPipeline']


project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGES_STORE = os.path.join(project_dir, 'pics')
IMAGES_EXPIRES = 90


DOWNLOAD_DELAY = 1.5  # 0.5*1.5 - 1.5*1.5 s
DOWNLOAD_TIMEOUT = 30  # 60s
COOKIES_ENABLED = False
CONCURRENT_REQUESTS_PER_DOMAIN = 5
USER_AGENTS_LIST_FILE = os.path.join(project_dir, 'user-agents.txt')
PROXY_LIST_FILE = os.path.join(project_dir, 'proxies.txt')
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Host': 'www.hao123.se',
    'If-None-Match': '1376403835|',
    'Proxy-Connection': 'keep-alive'}


# mongodb setting
MONGO_SERVER = 'localhost'
MONGO_PORT = 27017
MONGO_DB_NAME = 'xiaoshuo_pict'


DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'crawler.middleware.UserAgentsMiddleware': 400,
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'crawler.middleware.ProxyMiddleware': 100,
}
