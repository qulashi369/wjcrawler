#coding: utf8

from scrapy.spider import BaseSpider
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector

from crawler.items import Content, Chapter


class ChapterSpider(BaseSpider):
    name = "chapter"
    allowed_domains = ["hao123.se"]
    start_urls = ['http://www.hao123.se/8049/']
    cid = 100000
    bid = 8049

    def parse(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        items = []
        hxs = HtmlXPathSelector(response)
        chapters = hxs.select("//dl[@id='chapterlist']/dd/a")
        for chapter in chapters:
            title = chapter.select('text()').extract()[0]
            url = chapter.select('@href').extract()[0]
            self.cid += 1
            chapter_item = Chapter(cid=self.cid, bid=self.bid, title=title)
            yield chapter_item
            content_item = self.make_requests_from_url(url).replace(callback=self.parse_chapter)
            yield content_item

    def parse_chapter(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        hxs = HtmlXPathSelector(response)
        title = hxs.select("//div[@class='bookname']/h1/text()").extract()[0]
        content = hxs.select("//div[@id='content']/text()").extract()
        content = '<br>'.join(content)
        content_item = Content(cid=self.cid, content=content,
                               source=response.url)
        return content_item

