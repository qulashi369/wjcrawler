# /usr/bin/python
#-*-coding:utf-8

import MySQLdb
import pymongo
import logging
import shutil


logging.basicConfig(
    filename="/var/log/test.txt",
    level=logging.DEBUG,
    filemode='w+',
    format='%(asctime)s - %(levelname)s: %(message)s')


def init():
    conn = MySQLdb.connect(host='localhost', user='crawler', passwd='crawlerpwd',
                           db='xiaoshuo_test', port=3306, charset='utf8')
    cur = conn.cursor()
    client = pymongo.MongoClient("localhost", 27017)
    return conn, cur, client.xiaoshuo


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

        print qcatesql.format(**b)
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

        else:
            curbid = cur.fetchone()[0]  # 插入后的bookid

        # tmpbid = b['bid']  # 之前的bookid

        # 更改图片名字
        # if len(b['image_path']):
        #    syncpics(b['image_path'][0], str(curbid)+'.jpg')

        chapter(conn, cur, mdb, b['bid'], curbid, b['create_time'])


def chapter(conn, cur, mdb, tmpbid, curbid, create_time):
    sql = '''INSERT INTO chapter(book_id, title, content, create_time)VALUES (%s, %s, %s, %s);'''

    for ch in mdb.Chapter.find({"book_id": tmpbid}):
        ch['create_time'] = create_time
        # ch['title'] = ch['title'].encode("utf-8")
        ch['curbid'] = curbid
        for cont in mdb.Content.find({"cid": ch['cid'], 'book_id': tmpbid}):
            # ch['content'] = cont["content"].encode('utf-8')
            logging.debug(str(cont['cid']) + '-' + str(cont['book_id']))
            #查询当前章节是否存在
            num = cur.execute(
                "select id from chapter where book_id=%s and title=%s", (curbid, ch['title']))

            if num == 0:
                cur.execute(sql, (ch['curbid'], ch['title'], cont['content'], ch['create_time']))
                conn.commit()


#修改图片的名字
def syncpics(prefn, curfn):
    pfp = "/srv/salt/code/wyzq/crawler/book/pics/"
    cfp = "/var/www/img/covers/"
    shutil.copy(pfp + prefn, cfp + curfn)


if __name__ == "__main__":
    conn, cur, mdb = init()
    book(conn, cur, mdb)
    # chapter(conn, cur, mdb)
    cur.close()
    conn.close()
