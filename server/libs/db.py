# coding: utf8

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

_db = None
_session = None

_POOL_SIZE = 20
_POOL_RECYCLE = 3600


def get_db(db_url, debug=False):
    global _db
    if _db and str(_db.url) == db_url:
        return _db
    _db = create_engine(db_url, echo=debug,
                        pool_size=_POOL_SIZE, pool_recycle=_POOL_RECYCLE)
    return _db


def get_db_session(database_uri):
    global _session
    global _db
    if not _db or str(_db.url) != database_uri:
        _db = get_db(database_uri)
    if _session and _session.bind == _db:
        return _session
    Session = sessionmaker(bind=_db)
    _session = Session()
    return _session
