#coding:utf8

from pymongo import MongoClient
from items import Content, Chapter, Book
from settings import MONGO_SERVER, MONGO_PORT, MONGO_DB_NAME


class CrawlerPipeline(object):

    def __init__(self):
        self.client = MongoClient(MONGO_SERVER, MONGO_PORT)
        self.db = self.client[MONGO_DB_NAME]
        self.Chapter = self.db.Chapter
        self.Content = self.db.Content
        self.Book = self.db.Book

    def process_item(self, item, spider):
        if isinstance(item, Content):
            self.save_content(item)
        elif isinstance(item, Chapter):
            self.save_chapter(item)
        elif isinstance(item, Book):
            self.save_book(item)
        return item

    def save_content(self, item):
        self.Content.insert(dict(cid=item['cid'],
                                 content=item['content'],
                                 source=item['source']))

    def save_chapter(self, item):
        self.Chapter.insert(dict(cid=item['cid'],
                                 bid=item['bid'],
                                 title=item['title']))

    def save_book(self, item):
        self.Book.insert(dict(bid=item['bid'],
                              title=item['title']))
