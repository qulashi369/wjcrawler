# coding: utf8

from datetime import datetime

from sqlalchemy import types, Column, Index
from sqlalchemy.sql import exists
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash, check_password_hash

from database import db_session, Base


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
        category = Category.query.filter_by(id=self.category_id).one()
        return category

    @property
    def latest_chapter(self):
        # FIXME 这里有性能问题
        chapters = db_session.query(Chapter.id, Chapter.title
                                    ).filter_by(book_id=self.id)
        chapter = chapters.order_by(Chapter.id.desc()).first()
        return chapter

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

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def add(cls, username, password):
        # NOTE 此处password为加密后的密码hash
        user = cls(username, password)
        db_session.add(user)
        db_session.commit()

    @classmethod
    def get(cls, username):
        user = cls.query.filter_by(username=username).scalar()
        return user

    @classmethod
    def login(cls, username, password):
        user = cls.get(username)
        if user:
            return check_password_hash(user.password, password)
        return False

    @classmethod
    def check_username(cls, username):
        # TODO 检测user name 是否合法
        return True

    @classmethod
    def is_username_exists(cls, username):
        return db_session.query(
            exists().where(cls.username == username)
        ).scalar()

    @classmethod
    def register(cls, username, password):
        pw_hash = generate_password_hash(password)
        cls.add(username, pw_hash)


    def __repr__(self):
        return '<User(%r, %r)>' % (self.id, self.username)


Index('chapter_book_id', Chapter.book_id)
Index('username', User.username)
