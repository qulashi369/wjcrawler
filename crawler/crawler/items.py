#-*- coding: utf-8 -*-

from scrapy.item import Item, Field


class Content(Item):
    '''章节内容'''
    cid = Field()
    content = Field()
    source = Field()

    def __str__(self):
        return 'Content(source: %s)' % self['source']


class Chapter(Item):
    '''章节目录'''
    cid = Field()
    bid = Field()
    title = Field()

    def __str__(self):
        return 'Chapter (title: %s)' % self['title']
