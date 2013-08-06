#coding: utf8

from scrapy.spider import BaseSpider
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector

from crawler.items import Content


class ChapterSpider(BaseSpider):
    name = "chapter"
    allowed_domains = ["hao123.se"]
    start_urls = ['http://www.hao123.se/8049/']

    def parse(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        items = []
        hxs = HtmlXPathSelector(response)
        chapters = hxs.select("//dl[@id='chapterlist']/dd/a/@href").extract()
        items.extend([self.make_requests_from_url(url).replace(callback=self.parse_chapter)
                              for url in chapters])
        return items

    def parse_chapter(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        hxs = HtmlXPathSelector(response)
        title = hxs.select("//div[@class='bookname']/h1/text()").extract()[0]
        content = hxs.select("//div[@id='content']/text()").extract()
        content = '<br>'.join(content)
        content_item = Content(content=content, title=title, source=response.url)
        return [content_item]



class BookSpider(BaseSpider):
    name = 'book'
    allowed_domains = ["hao123.se"]
    start_urls = ['http://www.hao123.se/']
    def parse(self, response):
        filename = response.url.split("/")[-2]
        open(filename, 'wb').write(response.body)


