#-*- coding: utf-8 -*-

from scrapy.item import Item, Field

class Content(Item):
    # define the fields for your item here like:
    # name = Field()
    title = Field()
    content = Field()
    source = Field()

    def __str__(self):
        return 'Content(title: %s)' % self['title']
