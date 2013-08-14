#-*- coding: utf-8 -*-

from scrapy.item import Item, Field


class Book(Item):
    '''小说'''
    bid = Field()
    title = Field()
    author = Field()
    description = Field()
    create_time = Field()
    category = Field()
    source = Field()
    image_url = Field()
    image_path = Field()

    def __str__(self):
        return 'Book (title: %s)' % self['title'].encode('utf8')


class Chapter(Item):
    '''章节目录'''
    book_id = Field()
    cid = Field()
    title = Field()
    url = Field()

    def __str__(self):
        return 'Chapter (title: %s)' % self['title'].encode('utf8')
