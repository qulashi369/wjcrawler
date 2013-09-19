# coding: utf8

import re
from datetime import datetime

from sqlalchemy import types, Column, Index
from sqlalchemy.sql import exists
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from database import db_session, Base
from consts import (FROM_SITE, NORMAL)


class Book(Base):
    __tablename__ = 'book'
    id = Column(types.Integer, primary_key=True)
    title = Column(types.String(length=32))
    author = Column(types.String(length=32))
    description = Column(types.Text)
    category_id = Column(types.Integer)
    weight = Column(types.Integer, default=1)
    create_time = Column(types.DateTime)

    def __init__(self, title, author, description, category_id):
        self.title = title
        self.author = author
        self.description = description
        self.category_id = category_id
        self.create_time = datetime.now()

    @property
    def category(self):
        category = Category.query.filter_by(id=self.category_id).one()
        return category

    @property
    def first_chapter(self):
        chapters = db_session.query(Chapter.id, Chapter.title
                                    ).filter_by(book_id=self.id)
        chapter = chapters.first()
        return chapter

    @property
    def latest_chapter(self):
        chapters = db_session.query(Chapter.id, Chapter.title
                                    ).filter_by(book_id=self.id)
        chapter = chapters.order_by(Chapter.id.desc()).first()
        return chapter

    @classmethod
    def get(cls, book_id):
        book = cls.query.filter_by(id=book_id).scalar()
        return book

    @classmethod
    def gets(cls, book_ids):
        result = []
        for book_id in book_ids:
            book = cls.get(book_id)
            if book:
                result.append(book)
        return result

    def __repr__(self):
        return '<Book(%s, %s)>' % (self.title.encode('utf8'),
                                   self.author.encode('utf8'))


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

    @classmethod
    def get(cls, chapter_id, book_id):
        chapter = cls.query.filter_by(id=chapter_id, book_id=book_id).scalar()
        return chapter

    def next(self):
        chapters = db_session.query(Chapter.id, Chapter.book_id)
        try:
            chapter = chapters.filter(Chapter.book_id == self.book_id,
                                      Chapter.id > self.id
                                      ).limit(1).one()
        except NoResultFound:
            return None
        return chapter

    def previous(self):
        chapters = db_session.query(Chapter.id, Chapter.book_id
                                    ).order_by(Chapter.id.desc())
        try:
            chapter = chapters.filter(Chapter.book_id == self.book_id,
                                      Chapter.id < self.id
                                      ).limit(1).one()
        except NoResultFound:
            return None
        return chapter

    def __repr__(self):
        return '<Chapter(%r, %r)' % (self.title, self.book_id)


class Category(Base):
    __tablename__ = 'category'
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(length=32))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category(%r, %r)>' % (self.id, self.name)


class User(Base):
    __tablename__ = 'user'
    id = Column(types.Integer, primary_key=True)
    username = Column(types.String(length=32), unique=True)
    password = Column(types.String(length=64))
    registration = Column(types.String(length=8), default=FROM_SITE)
    email = Column(types.String(length=64))
    type = Column(types.Integer, default=NORMAL)
    create_time = Column(types.DateTime)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.create_time = datetime.now()

    @classmethod
    def add(cls, username, password, **kwargs):
        # NOTE 此处password为加密后的密码hash
        user = cls(username, password)
        for k, v in kwargs.items():
            user.k = v
        db_session.add(user)
        db_session.commit()
        return user

    @classmethod
    def get(cls, username):
        user = cls.query.filter_by(username=username).scalar()
        return user

    @classmethod
    def get_by_uid(cls, uid):
        user = cls.query.filter_by(id=uid).scalar()
        return user

    @classmethod
    def login(cls, username, password):
        user = cls.get(username)
        if user and check_password_hash(user.password, password):
            return user
        return None

    @classmethod
    def check_username(cls, username):
        '''中英文数字下划线混合，4-16字节'''
        if not 4 <= len(username.encode('gbk')) <= 16:
            return False
        p = re.compile(ur"^[\w\u4e00-\u9fa5]{2,16}$")
        return True if p.match(username) else False

    @classmethod
    def is_exists(cls, username):
        return db_session.query(
            exists().where(cls.username == username)
        ).scalar()

    @classmethod
    def register(cls, username, password):
        pw_hash = generate_password_hash(password)
        return cls.add(username, pw_hash)

    def get_favs(self):
        favs = Favourite.gets(self.id)
        return favs

    def __repr__(self):
        return '<User(%r, %r)>' % (self.id, self.username)


class Sentence(Base):
    __tablename__ = 'sentence'
    id = Column(types.Integer, primary_key=True)
    bid = Column(types.Integer)
    text = Column(types.Text)
    create_time = Column(types.DateTime)

    def __init__(self, bid, text):
        self.bid = bid
        self.text = text
        self.create_time = datetime.now()

    @classmethod
    def add(cls, bid, text):
        sentence = cls(bid, text)
        db_session.add(sentence)
        db_session.commit()
        return sentence


class Recommend(Base):
    __tablename__ = 'recommend'
    id = Column(types.Integer, primary_key=True)
    bid = Column(types.Integer)
    reason = Column(types.Text, default='')
    type = Column(types.String(length=8))  # 该推荐类别，可能不止显示在首页
    create_time = Column(types.DateTime)

    def __init__(self, bid):
        self.bid = bid
        self.create_time = datetime.now()

    @classmethod
    def add(cls, bid, **kwargs):
        recommend = cls(bid)
        for k, v in kwargs:
            recommend.k = v
        db_session.add(recommend)
        db_session.commit()
        return recommend


class Favourite(Base):
    __tablename__ = 'favourite'
    id = Column(types.Integer, primary_key=True)
    uid = Column(types.Integer)
    bid = Column(types.Integer)
    create_time = Column(types.DateTime)

    def __init__(self, uid, bid):
        self.uid = uid
        self.bid = bid
        self.create_time = datetime.now()

    def get_book(self):
        return Book.get(self.bid)

    @classmethod
    def get(cls, uid, bid):
        return cls.query.filter_by(uid=uid, bid=bid).scalar()

    @classmethod
    def gets(cls, uid):
        return cls.query.filter_by(uid=uid).all()

    @classmethod
    def add(cls, uid, bid, **kwargs):
        fav = cls(uid, bid)
        for k, v in kwargs:
            fav.k = v
        db_session.add(fav)
        db_session.commit()

    @classmethod
    def remove(cls, uid, bid):
        fav = cls.get(uid, bid)
        db_session.delete(fav)
        db_session.commit()

    @classmethod
    def get_bids(cls, uid):
        bids = db_session.query(Favourite.bid).filter_by(uid=uid).all()
        return [bid[0] for bid in bids]

    @classmethod
    def is_faved(cls, uid, bid):
        return db_session.query(
            exists().where(cls.uid == uid).where(cls.bid == bid)
        ).scalar()


class SourceSite(Base):
    __tablename__ = 'source_site'
    id = Column(types.Integer, primary_key=True)
    name = Column(types.String(length=32))
    url = Column(types.String(length=256), default='')
    chapter_rule = Column(types.String(length=128), default='')
    content_rule = Column(types.String(length=128), default='')
    create_time = Column(types.DateTime)

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.create_time = datetime.now()


class BookSource(Base):
    __tablename__ = 'book_source'
    id = Column(types.Integer, primary_key=True)
    bid = Column(types.Integer, nullable=False)
    source_site_id = Column(types.Integer)
    source_url = Column(types.String(length=128), nullable=False)
    create_time = Column(types.DateTime)

    def __init__(self, bid, source_site_id, source_url):
        self.bid = bid
        self.source_site_id = source_site_id
        self.source_url = source_url
        self.create_time = datetime.now()


class UpdateTask(Base):
    __tablename__ = 'update_task'
    id = Column(types.Integer, primary_key=True)
    bid = Column(types.Integer, nullable=False)
    latest_chapter = Column(types.String(length=128), nullable=False)
    source_url = Column(types.String(length=128), nullable=False)
    chapter_rule = Column(types.String(length=128), nullable=False)
    content_rule = Column(types.String(length=128), nullable=False)
    create_time = Column(types.DateTime)

    def __init__(self, bid, latest_chapter,
                 source_url, chapter_rule, content_rule):
        self.bid = bid
        self.latest_chapter = latest_chapter
        self.source_url = source_url
        self.chapter_rule = chapter_rule
        self.content_rule = content_rule
        self.create_time = datetime.now()


class UpdateLog(Base):
    __tablename__ = 'update_log'
    id = Column(types.Integer, primary_key=True)
    bid = Column(types.Integer, nullable=False)
    update_chapter_ids = Column(types.String(length=256))
    crawler_name = Column(types.String(length=64))
    create_time = Column(types.DateTime)

    def __init__(self, bid, update_chapter_ids, crawler_name):
        self.bid = bid
        self.update_chapter_ids = update_chapter_ids
        self.crawler_name = crawler_name
        self.create_time = datetime.now()


Index('chapter_book_id', Chapter.book_id)
Index('username', User.username)
Index('favourite', Favourite.uid, Favourite.bid, unique=True)
Index('book_source_bid', BookSource.bid)
