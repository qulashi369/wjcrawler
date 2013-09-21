#-*- coding: utf-8 -*-

from scrapy.item import Item, Field


class Content(Item):

    '''章节内容'''
    bid = Field()
    title = Field()
    content = Field()
    type = Field()
    crawler = Field()

    def __str__(self):
        return (
            'Content (bid: %d, crawler: %s)' % (self['bid'], self['crawler'])
        )
