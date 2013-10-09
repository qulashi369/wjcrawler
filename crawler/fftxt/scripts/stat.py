#-*-coding:utf8


def stat():
    '''统计数据'''    
    import pymongo
    connection = pymongo.Connection('localhost', 27017)
    db = connection.xiaoshuo_fftxt
    delbooks = []
    for b in db.book.find().sort('id'):
        chapter_count = db.chapter.find({"bid": b['id']}).count()
        print b['id'], '\t', b['name'].encode("utf-8"), chapter_count, "\t"
        if chapter_count < 20:
            delbooks.append(b['id'])
    print 'book count:', db.book.find().count()
    print '删除的书:', delbooks
    delbook(db, delbooks)

def delbook(db, bids):
    for bid in bids:
        db.book.remove({"id": bid})
        db.chapter.remove({"bid": bid})

if __name__ == "__main__":
    stat()
