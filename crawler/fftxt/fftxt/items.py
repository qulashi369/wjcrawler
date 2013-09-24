# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class FftxtItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass


class Book(Item):
    mongoname = 'book'
    id = Field()
    name = Field()
    author = Field()
    category = Field()
    desc = Field()
    status = Field()
    create_time = Field()
    source = Field()


class Chapter(Item):
    mongoname = 'chapter'
    id = Field()
    bid = Field()
    name = Field()
    content = Field()
