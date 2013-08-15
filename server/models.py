# coding: utf8

from sqlalchemy import types, Column
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'
    id = Column(types.Integer, primary_key=True)
    title = Column(types.String(length=32))
    author = Column(types.String(length=32))
    create_time = Column(types.DateTime)

    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.datetime = datetime.now()

    def __repr__(self):
        return '<Book(%r, %r)>' % (self.title, self.author)


def init_tables():
    from db import get_db
    from config import DB_URL
    _db = get_db(DB_URL)
    Base.metadata.create_all(_db)


if __name__ == '__main__':
    pass
    #init_tables()
