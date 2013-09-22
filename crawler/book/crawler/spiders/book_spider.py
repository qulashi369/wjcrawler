# coding: utf8

import urllib
from datetime import datetime

from scrapy.spider import BaseSpider
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request

from crawler.items import Book, Chapter, Content
from crawler.pipelines import get_db_book, get_db_chapter, get_db_content
from books import books as pybooks

_book_title_xpath = "//div[@class='book_news_style_text2']/h1/text()"
_book_info_xpath = "//div[@class='book_news_style_text2']/h2/text()"
_book_desc_xpath = "//div[@class='msgarea']/p/text()"
_book_pic_xpath = "//div[@class='book_news_style_img1']/img/@src"
_chapters_xpath = "//dl[@id='chapterlist']/dd/a"
_content_xpath = "//div[@id='content']/text()"
_search_result_xpath = "//div[@class='book_news_style_text']/h1/a/@href"


class BookSpider(BaseSpider):
    '''抓取书本页基本信息'''
    name = "book"
    allowed_domains = ["hao123.se"]
    search_url = r'http://www.hao123.se/modules/article/search.php?'

    def start_requests(self):
        books = pybooks
        for book in books:
            name = book.decode("utf-8").encode("gb2312", "ignore")
            encode_name = urllib.quote(name)
            args = r"searchkey=%s&searchtype=1" % encode_name
            url = self.search_url + args
            yield Request(url=url, callback=self.parse_book)

    def parse_book(self, response):
        response.replace(body=response.body.decode('gbk', 'ignore').encode('utf-8'))
        hxs = HtmlXPathSelector(response)

        if response.url.startswith('http://www.hao123.se/modules/article/search.php?'):
            # 出现搜索结果页
            result = hxs.select(_search_result_xpath).extract()
            if len(result):
                url = result[0]
                url = 'http://www.hao123.se' + url
                yield Request(url=url, callback=self.parse_book)
            else:
                log.msg("No book result in  %s" % response.url,
                        level=log.WARNING)
        else:
            # 直接跳转到书本页
            book_title = hxs.select(_book_title_xpath).extract()[0]
            book_author = hxs.select(_book_info_xpath).extract()[0]
            book_category = hxs.select(_book_info_xpath).extract()[1]
            book_desc_result = hxs.select(_book_desc_xpath).extract()
            if book_desc_result:
                # 有可能木有书本描述
                book_desc = book_desc_result[0]
            else:
                book_desc = ''
            image_url = hxs.select(_book_pic_xpath).extract()[0]
            book_id = response.url.rsplit('/', 2)[1]
            source = response.url
            yield Book(bid=book_id, title=book_title, author=book_author,
                       category=book_category, description=book_desc,
                       create_time=datetime.now(), source=source,
                       image_url=image_url)


class ChapterSpider(BaseSpider):
    '''抓取书籍目录'''
    name = "chapter"
    allowed_domains = ["hao123.se"]

    def __init__(self):
        self.Book = get_db_book()
        self.Chapter = get_db_chapter()

    def start_requests(self):
        for book in self.Book.find():
            url = book.get('source')
            if self.Chapter.find_one({"book_id": book.get('bid')}):
                print 'already crawl chapters: %s' % book.get('title')
            else:
                yield Request(url=url, callback=self.parse_chapters)

    def parse_chapters(self, response):
        response.replace(body=response.body.decode('gbk', 'ignore').encode('utf-8'))
        hxs = HtmlXPathSelector(response)
        chapters = hxs.select(_chapters_xpath)
        for cid, chapter in enumerate(chapters):
            title = chapter.select('text()').extract()[0]
            url = chapter.select('@href').extract()[0]
            book_id = response.url.rsplit('/', 2)[1]
            yield Chapter(book_id=book_id, title=title, cid=cid, url=url)


class ContentSpider(BaseSpider):
    '''抓取章节内容'''
    name = "content"
    allowed_domains = ["hao123.se"]

    def __init__(self):
        self.Chapter = get_db_chapter()
        self.Content = get_db_content()

    def start_requests(self):
        for chapter in self.Chapter.find():  # 左开右闭， [0:5): 0,1,2,3,4
            cid = chapter.get('cid')
            book_id = chapter.get('book_id')
            if self.Content.find_one({"cid": cid, "book_id": book_id}):
                print 'already crawl content: %s' % chapter.get('title')
            else:
                url = chapter.get('url')
                yield Request(url=url, meta={'cid': cid, 'book_id': book_id},
                              callback=self.parse_content)

    def parse_content(self, response):
        response.replace(body=response.body.decode('gbk', 'ignore').encode('utf-8'))
        cid = response.meta['cid']
        book_id = response.meta['book_id']
        hxs = HtmlXPathSelector(response)
        content = hxs.select("//div[@id='content']/text()").extract()
        content = '<br><br>'.join(content)
        content_item = Content(cid=cid, content=content, book_id=book_id)
        yield content_item
