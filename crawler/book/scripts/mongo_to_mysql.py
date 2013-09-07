# /usr/bin/python
#-*-coding:utf-8

import MySQLdb
import pymongo
import logging
import shutil
from logging import FileHandler
import time


book_handler = FileHandler("/home/yj/b_%s" % time.strftime("%Y%m%d%H%M", time.localtime()), "a+")
chapter_handler = FileHandler("/home/yj/c_%s" % time.strftime("%Y%m%d%H%M", time.localtime()), "a+")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
book_handler.setFormatter(formatter)
book_handler.setLevel(logging.INFO)
chapter_handler.setFormatter(formatter)
chapter_handler.setLevel(logging.INFO)
book_logger = logging.getLogger("book")
book_logger.addHandler(book_handler)
chapter_logger = logging.getLogger("chapter")
chapter_logger.addHandler(chapter_handler)

def init():
    conn = MySQLdb.connect(host='localhost', user='crawler', passwd='crawlerpwd',
                           db='xiaoshuo', port=3306, charset='utf8')
    cur = conn.cursor()
    client = pymongo.MongoClient("localhost", 27017)
    return conn, cur, client.xiaoshuo1


def book(conn, cur, mdb):
    ibooksql = '''INSERT INTO book(
            title, author, description, category_id, create_time)
    VALUES (\'{title}\', \'{author}\', \'{description}\', \'{category}\', \'{create_time}\');'''

    icatesql = "INSERT INTO category( name ) VALUES('{category}')"
    qcatesql = "SELECT id FROM category WHERE name='{category}'"
    cid = -1  # category id
    curbid = -1
    for b in mdb.Book.find():
        for k in ["title", "author", "description", "category"]:
            b[k] = b[k].encode('utf-8')

        #查询当前的书的category是否存在.不存在插入新category
        if 0 == cur.execute(qcatesql.format(**b)):
            cur.execute(icatesql.format(**b))
            conn.commit()
            cid = cur.lastrowid

        else:
            cid = cur.fetchone()[0]

        # 获取cate_id
        b['category'] = cid
        num = cur.execute("select id from book where title=%s", (b['title'],))

        #获取当前书的id
        if num == 0:
            cur.execute(ibooksql.format(**b))
            conn.commit()
            curbid = cur.lastrowid
            book_logger.info("新书: %s --- 作者: %s" % (b['title'], b['author']))
            chapter_logger.info("新书: %s --- 作者: %s" % (b['title'], b['author']))

        else:
            curbid = cur.fetchone()[0]  # 插入后的bookid

        # tmpbid = b['bid']  # 之前的bookid

        # 更改图片名字
        # if len(b['image_path']):
        #    syncpics(b['image_path'][0], str(curbid)+'.jpg')

        chapter(conn, cur, mdb, b['bid'], curbid, b['create_time'], b['title'])


def chapter(conn, cur, mdb, tmpbid, curbid, create_time, btitle):
    sql = '''INSERT INTO chapter(book_id, title, content, create_time)VALUES (%s, %s, %s, %s);'''

    for ch in mdb.Chapter.find({"book_id": tmpbid}):
        ch['create_time'] = create_time
        ch['curbid'] = curbid
        for cont in mdb.Content.find({"cid": ch['cid'], 'book_id': tmpbid}):
            logging.debug(str(cont['cid']) + '-' + str(cont['book_id']))
            #查询当前章节是否存在
            num = cur.execute(
                "select id from chapter where book_id=%s and title=%s", (curbid, ch['title']))

            if num == 0:
                cur.execute(sql, (ch['curbid'], ch['title'], cont['content'], ch['create_time']))
                conn.commit()
                chapter_logger.info("新章节: %s --- 书名: %s" % (ch['title'].encode('utf-8'), btitle))


#修改图片的名字
def syncpics(prefn, curfn):
    pfp = "/srv/salt/code/wyzq/crawler/book/pics/"
    cfp = "/var/www/img/covers/"
    shutil.copy(pfp + prefn, cfp + curfn)


if __name__ == "__main__":
    #conn, cur, mdb = init()
    #book(conn, cur, mdb)
    #cur.close()
    #conn.close()
    book_logger.info("test")
    chapter_logger.info("test")
