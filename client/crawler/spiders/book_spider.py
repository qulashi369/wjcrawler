# coding: utf8

import re
import json
from urlparse import urljoin

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import requests


limit = 5
CRAWLER = 'xz'


def get_tasks():
    url = 'http://localhost:8000/api/update/tasks?limit=%d' % limit
    resp = requests.get(url)
    return resp.json().get('tasks')


def is_same_chapter(chapter, latest_chapter):
    chars = r'[!,.()!?，。『』「」‘’“”"\'T\s]'
    chapter = re.sub(chars, '', chapter)
    latest_chapter = re.sub(chars, '', latest_chapter)
    if chapter[-5:] == latest_chapter[-5:]:
        return True
    return False


def get_new_chapters(chapters, latest_chapter):
    new_chapters = []
    for title, url in chapters:
        if is_same_chapter(title, latest_chapter):
            break
        else:
            new_chapters.insert(0, (title, url))
    if len(new_chapters) == len(chapters):
        raise
    return new_chapters


def update(bid, content, title, crawler, type):
    url = 'http://localhost:8000/api/update/%d' % int(bid)
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = dict(
        crawler=crawler,
        chapter={
            'type': type,
            'title': title,
            'content': content
        }
    )
    data = json.dumps(data)
    resp = requests.post(url, data, headers=headers)
    assert resp.status_code == 200, 'HTTP ERROR!!'


class ChapterSpider(BaseSpider):
    '''抓取书籍目录'''
    name = "chapter"
    allowed_domains = ["fftxt.net", "hao123.se"]

    def __init__(self):
        self.tasks = get_tasks()

    def start_requests(self):
        for book in self.tasks:
            bid = book.get('bid')
            source_site = book.get('source_site')
            latest_chapter = book.get('latest_chapter')
            url = book.get('source_url')
            if source_site == 'fftxt.net':
                callback = self.parse_fftxt
            elif source_site == 'hao123.se':
                callback = self.parse_hao123
            yield Request(
                url=url, callback=callback,
                meta={'bid': bid, 'latest_chapter': latest_chapter}
            )

    def parse_fftxt(self, response):
        bid = response.meta['bid']
        latest_chapter = response.meta['latest_chapter']

        response.replace(
            body=response.body.decode('gbk', 'ignore').encode('utf-8')
        )
        hxs = HtmlXPathSelector(response)
        selectors = hxs.select("//ul[@id='chapterlist']/li/a")
        chapters = []
        for selector in selectors:
            title = selector.select('text()').extract()[0]
            url = urljoin(response.url, selector.select('@href').extract()[0])
            chapters.insert(0, (title, url))
        try:
            new_chapters = get_new_chapters(chapters, latest_chapter)

            chapter_requests = []
            for title, url in new_chapters:
                chapter_requests.insert(0,
                    Request(
                        url=url, callback=self.parse_fftxt_content,
                        meta={'bid': bid, 'title': title}
                    )
                )
            return chapter_requests
        except:
            print 'Error: \n URL %s \n seems can not match chapter %s' % (
                response.url, latest_chapter)

    def parse_fftxt_content(self, response):
        bid = response.meta['bid']
        title = response.meta['title']
        response.replace(
            body=response.body.decode('gbk', 'ignore').encode('utf-8')
        )
        hxs = HtmlXPathSelector(response)
        content = hxs.select("//div[@class='novel_content']/text()").extract()
        # content[0] : '一秒记住【非凡TXT下载】www.fftxt.net，为您提供精彩小说阅读。'
        content = '<br><br>'.join(content[1:])
        update(bid, content, title, CRAWLER, 'text')

    def parse_hao123(self, response):
        # TODO
        pass
