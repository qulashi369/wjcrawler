#-*-coding:utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from fftxt.items import Book, Chapter
from utils import filter_tags
from fftxt.db import get_conn
from datetime import datetime


class BookSpider(CrawlSpider):
    name = 'fftxt'
    allowed_domains = ['fftxt.net']

    def __init__(self, category="books.txt", *args, **kwargs):
        self.category = open(category)

    def start_requests(self):
        host = "http://www.fftxt.net/book/"
        for book in self.category:
            book = book.strip('\n')
            if book[0] != '#':
                bid = book.split(":")[1]
                if get_conn("book").find({'id': bid}).count():
                    print book, ' already exists'
                    continue
                url = host + bid + "/"
                req = Request(url, callback=self.parse_book)
                req.meta['target'] = url
                req.meta['bid'] = bid
                yield req

    def parse_book(self, response):
        hxs = HtmlXPathSelector(response)
        bmeta = hxs.select("//div[@class='book_news_style_text2']")
        other = bmeta.select("//h2/text()").extract()
        book = Book()
        book['id'] = response.meta['bid']
        book['create_time'] = datetime.now()
        book['author'] = other[0]
        book['category'] = other[1]
        book['status'] = other[2]
        book['name'] = bmeta.select("//h1/text()").extract()[0]
        book['desc'] = hxs.select("//div[@class='msgarea']/p/text()").extract()[0]
        book['source'] = response.meta['target']
        chapters = hxs.select("//ul[@id='chapterlist']/li/a/@href").extract()
        yield book
        for ch in chapters:
            churl = response.meta['target'] + ch
            req = Request(url=churl, callback=self.parse_chapter)
            req.meta['book'] = book
            req.meta['cid'] = ch.split('.')[0]
            yield req

    def parse_chapter(self, response):
        chapter = Chapter()
        hxs = HtmlXPathSelector(response)
        chapter['name'] = hxs.select("//h1[@class='novel_title']/text()").extract()[0]
        content = hxs.select("//div[@class='novel_content']").extract()
        #chapter['content'] = filter_tags(content[0])[39:]  # 前面39个字符是广告
        chapter['content'] = content[0][69:]  # 前面66个字符是广告
        chapter['id'] = response.meta['cid']
        chapter['bid'] = response.meta['book']['id']
        yield chapter
