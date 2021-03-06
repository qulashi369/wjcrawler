# coding: utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL


engine = create_engine(DATABASE_URL, convert_unicode=True,
                       pool_size=20, pool_recycle=7200)
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
