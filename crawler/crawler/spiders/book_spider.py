#coding: utf8

import urllib

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from crawler.items import Content, Chapter, Book
from books import books


class ChapterSpider(BaseSpider):
    name = "chapter"
    allowed_domains = ["hao123.se"]
    search_url = r'http://www.hao123.se/modules/article/search.php?'

    def __init__(self):
        self.books = books

    def start_requests(self):
        for bid, book in enumerate(self.books):
            name = book.decode("utf-8").encode("gb2312", "ignore")
            encode_name = urllib.quote(name)
            args = r"searchkey=%s&searchtype=1" % encode_name
            url = self.search_url + args
            yield Request(url=url, meta={"bid": bid},
                          callback=self.parse_book)

    def parse_book(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        hxs = HtmlXPathSelector(response)
        book_title = hxs.select("//div[@class='book_news_style_text2']/h1/text()").extract()[0]
        chapters = hxs.select("//dl[@id='chapterlist']/dd/a")
        bid = response.meta['bid']
        yield Book(bid=bid, title=book_title)
        for cid, chapter in enumerate(chapters):
            title = chapter.select('text()').extract()[0]
            url = chapter.select('@href').extract()[0]
            chapter_item = Chapter(cid=cid, bid=bid, title=title)
            yield chapter_item
            yield Request(url, meta={'cid': cid},
                          callback=self.parse_chapter)

    def parse_chapter(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        cid = response.meta['cid']
        hxs = HtmlXPathSelector(response)
        content = hxs.select("//div[@id='content']/text()").extract()
        content = '<br>'.join(content)
        content_item = Content(cid=cid, content=content,
                               source=response.url)
        yield content_item
