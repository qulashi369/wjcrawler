#coding:utf8

from pymongo import MongoClient
from items import Content, Chapter

class CrawlerPipeline(object):
    db_name = 'xiaoshuo'

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[self.db_name]
        self.Chapter = self.db.Chapter
        self.Content = self.db.Content

    def process_item(self, item, spider):
        if isinstance(item, Content):
            self.Content.insert(dict(cid=item['cid'],
                                     content=item['content'],
                                     source=item['source']))

        elif isinstance(item, Chapter):
            self.Chapter.insert(dict(cid=item['cid'],
                                     bid=item['bid'],
                                     title=item['title']))
        return item
