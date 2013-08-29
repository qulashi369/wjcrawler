# coding: utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URL


engine = create_engine(DB_URL, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_tables():
    '''创建所以表，只需要运行一次！'''
    from sqlalchemy import event
    from sqlalchemy import DDL
    import models

    event.listen(
        models.Book.__table__,
        "after_create",
        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10001;")
    )
    event.listen(
        models.Chapter.__table__,
        "after_create",
        DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10001;")
    )
    Base.metadata.create_all(bind=engine)
