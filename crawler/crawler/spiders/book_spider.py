#coding: utf8

from scrapy.spider import BaseSpider
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request, FormRequest

from crawler.items import Content, Chapter
import urllib, sys

class ChapterSpider(BaseSpider):
    name = "chapter"
    allowed_domains = ["hao123.se"]
    search_url = r'http://www.hao123.se/modules/article/search.php?'

    def __init__(self, books):
        self.books = open(books,'r')

    
    def start_requests(self):

        for bid, book in enumerate(self.books):
            
            if book[0] <> "#": 
                book = book.replace("\n", "")
                name = book.decode("utf-8").encode("gb2312", "ignore")
                encode_name = urllib.quote(name)
                args = r"searchkey=%s&searchtype=1"%encode_name
                url=self.search_url + args
                yield Request(url=url, meta={"bid":bid},
                                callback=self.parse_book)

    
    def parse_book(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        items = []
        hxs = HtmlXPathSelector(response)
        chapters = hxs.select("//dl[@id='chapterlist']/dd/a")
        bid = response.meta['bid']

        for cid, chapter in enumerate(chapters):
            title = chapter.select('text()').extract()[0]
            url = chapter.select('@href').extract()[0]
            chapter_item = Chapter(cid=cid, bid=bid, title=title)
            yield chapter_item
            yield Request(url, meta={'cid':cid},
                          callback=self.parse_chapter)


    def parse_chapter(self, response):
        response.replace(body=response.body.decode('gbk').encode('utf-8'))
        cid = response.meta['cid']
        hxs = HtmlXPathSelector(response)
        title = hxs.select("//div[@class='bookname']/h1/text()").extract()[0]
        content = hxs.select("//div[@id='content']/text()").extract()
        content = '<br>'.join(content)
        content_item = Content(cid=cid, content=content,
                               source=response.url)
        yield content_item

