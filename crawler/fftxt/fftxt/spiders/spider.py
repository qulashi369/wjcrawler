#-*-coding:utf-8
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from fftxt.items import Book, Chapter
#from utils import filter_tags
from fftxt.db import get_conn
from datetime import datetime
from htmlparser import strip_special_tags


class BookSpider(CrawlSpider):
    name = 'fftxt'
    allowed_domains = ['fftxt.net']

    def __init__(self, category="bs.txt", *args, **kwargs):
        self.category = open(category)

    def start_requests(self):
        host = "http://www.fftxt.net/book/"
        for book in self.category:
            book = book.strip('\n')
            if book[0] != '#':
                bid = book.split(":")[1]
                if get_conn("book").find({'id': int(bid)}).count():
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
        book['id'] = int(response.meta['bid'])
        book['create_time'] = datetime.now()
        book['author'] = other[0][3:]
        book['category'] = other[1][3:]
        book['status'] = other[2][5:]
        book['name'] = bmeta.select("//h1/text()").extract()[0]
        desc = hxs.select("//div[@class='msgarea']/p/text()").extract()
        if desc:
            book['desc'] = strip_special_tags(desc[0])
        else:
            book['desc'] = ''
        book['source'] = response.meta['target']
        #chapters = hxs.select("//ul[@id='chapterlist']/li/a/@href").extract()
        chapters = hxs.select("//ul[@id='chapterlist']/li/a")
        yield book
        for ch in chapters:
            url = ch.select("@href").extract()[0]
            cname = ch.select("@title").extract()[0]
            churl = response.meta['target'] + url
            req = Request(url=churl, callback=self.parse_chapter)
            req.meta['book'] = book
            req.meta['cid'] = url.split('.')[0]
            req.meta['cname'] = cname
            yield req

    def parse_chapter(self, response):
        chapter = Chapter()
        hxs = HtmlXPathSelector(response)
        chapter['name'] = response.meta['cname']
        content = hxs.select("//div[@class='novel_content']").extract()
        #chapter['content'] = filter_tags(content[0])[39:]  # 前面39个字符是广告
        chapter['content'] = content[0][69:]  # 前面66个字符是广告
        chapter['id'] = int(response.meta['cid'])
        chapter['bid'] = int(response.meta['book']['id'])
        yield chapter
