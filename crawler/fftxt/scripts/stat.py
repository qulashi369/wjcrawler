#-*-coding:utf8


def stat():
    '''统计数据'''    
    import pymongo
    connection = pymongo.Connection('localhost', 27017)
    db = connection.xiaoshuo_fftxt
    for b in db.book.find().sort('id'):
        chapter_count = db.chapter.find({"bid": b['id']}).count()
        print b['id'], '\t', b['name'].encode("utf-8"), chapter_count, "\t"
    print 'book count:', db.book.find().count()

if __name__ == "__main__":
    stat()
