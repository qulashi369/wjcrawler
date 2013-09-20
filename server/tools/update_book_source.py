# coding : utf8

import os
os.sys.path.append(os.getcwd())

from pymongo import MongoClient

from models import BookSource, Book


MONGO_DBS = ['xiaoshuo', 'xiaoshuo1', 'xiaoshuo2', 'xiaoshuo3', 'xiaoshuo4']
client = MongoClient('localhost', 27017)

source_site = 'hao123.se'
base_url = 'http://www.hao123.se/%s/'


all_books = Book.gets()

for book in all_books:
    title = book.title
    bid = book.id
    for db in MONGO_DBS:
        book_table = client[db].Book
        book_in_mongo = book_table.find_one({"title": title})
        if book_in_mongo:
            source_url = base_url % book_in_mongo.bid
            BookSource.add(bid, source_site, source_url)
        else:
            continue
