# coding: utf8

from datetime import datetime

from sqlalchemy import types, Column, Index
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URL
from libs.db import get_db_session

Base = declarative_base()
db_session = get_db_session(DB_URL)


class Book(Base):
    __tablename__ = 'book'
    id = Column(types.Integer, primary_key=True)
    title = Column(types.String(length=32))
    author = Column(types.String(length=32))
    description = Column(types.Text)
    category_id = Column(types.Integer)
    create_time = Column(types.DateTime)

    def __init__(self, title, author, description, category_id):
        self.title = title
        self.author = author
        self.description = description
        self.category_id = category_id
        self.create_time = datetime.now()

    @property
    def category(self):
        category = db_session.query(Category).filter_by(id=self.category_id).one()
        return category

    @property
    def latest_chapter(self):
        # FIXME 这里有性能问题
        chapters = db_session.query(Chapter.id, Chapter.title).filter_by(book_id=self.id)
        chapter = chapters.order_by(Chapter.id.desc()).first()
        return chapter

    def __repr__(self):
        return '<Book(%s, %s)>' % (self.title.encode('utf8'), self.author.encode('utf8'))


class Chapter(Base):
    __tablename__ = 'chapter'
    id = Column(types.Integer, primary_key=True)
    book_id = Column(types.Integer)
    title = Column(types.String(length=128))
    content = Column(types.Text)
    create_time = Column(types.DateTime)

    def __init__(self, book_id, title, content):
        self.book_id = book_id
        self.title = title
        self.content = content
        self.create_tile = datetime.now()

    def __repr__(self):
        return '<Chapter(%r, %r)' % (self.title, self.book_id)


# 为book_id 加索引
Index('chapter_book_id', Chapter.book_id)


class Category(Base):
    __tablename__ = 'category'
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(length=32))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category(%r, %r)>' % (self.id, self.name)


if __name__ == '__main__':
    '''创建所以表，只需要运行一次！'''
    from sqlalchemy import event
    from sqlalchemy import DDL

    def init_tables():
        from libs.db import get_db
        from config import DB_URL
        _db = get_db(DB_URL)
        Base.metadata.create_all(_db)

    event.listen(
        Book.__table__,
        "after_create",
        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10001;")
    )
    event.listen(
        Chapter.__table__,
        "after_create",
        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10001;")
    )
    init_tables()
