#coding:utf8

from pymongo import MongoClient
from items import Content, Chapter
from settings import MONGO_SERVER, MONGO_PORT, MONGO_DB_NAME


class CrawlerPipeline(object):

    def __init__(self):
        self.client = MongoClient(MONGO_SERVER, MONGO_PORT)
        self.db = self.client[MONGO_DB_NAME]
        self.Chapter = self.db.Chapter
        self.Content = self.db.Content

    def process_item(self, item, spider):
        if isinstance(item, Content):
            self.save_content(item)
        elif isinstance(item, Chapter):
            self.save_chapter(item)
        return item

    def save_content(self, item):
        self.Content.insert(dict(cid=item['cid'],
                                 content=item['content'],
                                 source=item['source']))

    def save_chapter(self, item):
        self.Chapter.insert(dict(cid=item['cid'],
                                 bid=item['bid'],
                                 title=item['title']))
