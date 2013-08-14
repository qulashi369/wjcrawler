#coding:utf8

from cStringIO import StringIO

from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline, ImageException
from pymongo import MongoClient

from items import Book
from settings import MONGO_SERVER, MONGO_PORT, MONGO_DB_NAME

db_book = None
db_chapter = None


def get_db_book():
    global db_book
    if not db_book:
        client = MongoClient(MONGO_SERVER, MONGO_PORT)
        db = client[MONGO_DB_NAME]
        db_book = db.Book
    return db_book

def get_db_chapter():
    global db_chapter
    if not db_chapter:
        client = MongoClient(MONGO_SERVER, MONGO_PORT)
        db = client[MONGO_DB_NAME]
        db_chapter = db.Chapter
    return db_chapter




class BookPipeline(object):

    def __init__(self):
        self.Book = get_db_book()

    def process_item(self, item, spider):
        author = item['author'].encode('utf8').replace('作者:', '')
        category = item['category'].encode('utf8').replace('所属:', '')
        title = item['title'].encode('utf8').replace('《', '').replace('》', '')
        self.Book.insert(dict(bid=item['bid'],
                              title=title,
                              author=author,
                              category=category,
                              source=item['source'],
                              image_path=item['image_path'],
                              description=item['description'],
                              create_time=item['create_time']))



class MyImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if self.is_in_db(item):
            raise DropItem("Duplicate item found: %s" % item)
        if item.get('image_url'):
            yield Request(item['image_url'])

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        item['image_path'] = image_path
        return item

    def is_in_db(self, item):
        bid = str(item['bid'])
        if get_db_book().find_one({"bid": bid}):
            return True
        return False


class ChapterPipeline(object):
    def __init__(self):
        self.Chapter = get_db_chapter()

    def process_item(self, item, spider):
        if self.is_in_db(item):
            raise DropItem("Duplicate item found: %s" % item)

        self.Chapter.insert(dict(title=item['title'], url=item['url'],
                                 book_id=item['book_id'], cid=item['cid']))
        return item

    def is_in_db(self, item):
        url = str(item['url'])
        if get_db_chapter().find_one({"url": url}):
            return True
        return False

