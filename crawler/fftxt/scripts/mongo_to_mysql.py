# /usr/bin/python
#-*-coding:utf-8

import MySQLdb
import pymongo
import logging
import shutil
from logging import FileHandler
import time


book_log_path = "/tmp/b_%s"
chapter_log_path = "/tmp/c_%s"
logformat = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
book_handler = FileHandler(book_log_path % time.strftime("%Y%m%d", time.localtime()), "a+")
chapter_handler = FileHandler(chapter_log_path % time.strftime("%Y%m%d", time.localtime()), "a+")
formatter = logging.Formatter(logformat)
book_handler.setFormatter(formatter)
book_handler.setLevel(logging.INFO)
chapter_handler.setFormatter(formatter)
chapter_handler.setLevel(logging.INFO)
book_logger = logging.getLogger("book")
book_logger.setLevel(logging.DEBUG)
book_logger.addHandler(book_handler)
chapter_logger = logging.getLogger("chapter")
chapter_logger.setLevel(logging.DEBUG)
chapter_logger.addHandler(chapter_handler)


def init():
    conn = MySQLdb.connect(
        host='localhost', user='crawler', passwd='crawlerpwd',
        db='xiaoshuo_fftxt', port=3306, charset='utf8')
    cur = conn.cursor()
    client = pymongo.MongoClient("localhost", 27017)
    return conn, cur, client.xiaoshuo_fftxt


def book(conn, cur, mdb):
    ibooksql = '''INSERT INTO book(
            title, author, description, category_id, create_time)
    VALUES (\'{name}\', \'{author}\', \'{desc}\', \'{category}\', \'{create_time}\');'''

    icatesql = "INSERT INTO category( name ) VALUES('{category}')"
    qcatesql = "SELECT id FROM category WHERE name='{category}'"
    cid = -1  # category id
    curbid = -1
    for b in mdb.book.find():
        #TODO 少了desc
        for k in ["name", "author", "category", "status"]:
            b[k] = b[k].encode('utf-8')
        if len(b['desc']) > 100:
            b['desc'] = b['desc'].encode('utf-8')
        elif len(b['desc']) == 1:
            b['desc'] = b['desc'][0].encode('utf-8')
        else:
            b['desc'] = ''

        #查询当前的书的category是否存在.不存在插入新category
        if 0 == cur.execute(qcatesql.format(**b)):
            cur.execute(icatesql.format(**b))
            conn.commit()
            cid = cur.lastrowid
        else:
            cid = cur.fetchone()[0]

        # 获取cate_id
        b['category'] = cid
        num = cur.execute("select id from book where title=%s", (b['name'],))

        #获取当前书的id
        if num == 0:
            cur.execute(ibooksql.format(**b))
            conn.commit()
            curbid = cur.lastrowid
            book_logger.info("新书: %s --- 作者: %s" % (b['name'], b['author']))
            chapter_logger.info(
                "新书: %s --- 作者: %s" % (b['name'], b['author']))
        else:
            curbid = cur.fetchone()[0]  # 插入后的bookid

        print curbid
        # 更改图片名字
        # if len(b['image_path']):
        #    syncpics(b['image_path'][0], str(curbid)+'.jpg')
        # syncpics("full/" + b['bid'], str(curbid) + '.jpg')
        chapter(conn, cur, mdb, curbid, b)


def chapter(conn, cur, mdb, curbid, b):
    sql = '''INSERT INTO chapter(book_id, title, content, create_time)VALUES (%s, %s, %s, %s);'''

    for ch in mdb.chapter.find({"bid": b['id']}):
        ch['create_time'] = b['create_time']
        ch['curbid'] = curbid
        #查询当前章节是否存在
        num = cur.execute("select id from chapter where book_id=%s and title=%s", (curbid, ch['name']))
        if num == 0:
            cur.execute(sql, (ch['curbid'], ch['name'], ch['content'], ch['create_time']))
            conn.commit()
            chapter_logger.info("新章节: %s --- 书名: %s" %
                                (ch['name'].encode('utf-8'), b['name']))


#修改图片的名字
def syncpics(prefn, curfn):
    print prefn, curfn
    pfp = "/home/yj/wyzq/crawler/book/pics/"
    cfp = "/var/www/img/covers/"
    # cfp = "/tmp/"
    shutil.copy(pfp + prefn, cfp + curfn)


if __name__ == "__main__":
    conn, cur, mdb = init()
    book(conn, cur, mdb)
    cur.close()
    conn.close()
