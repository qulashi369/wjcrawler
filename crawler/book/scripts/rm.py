#-*-coding:utf8

def rm_nullcontent():
    import pymongo
    connection=pymongo.Connection('localhost',27017)
    db = connection.xiaoshuo1
    bids = []
    for b in db.Book.find():
        content_count = db.Content.find({'book_id':b['bid']}).count()
        if content_count == 0:
            print "正在删除 ", b['title']
            db.Chapter.remove({'book_id':b['bid']})
            db.Content.remove({'book_id':b['bid']})
            bids.append(b['bid'])
    for bid in bids:
        print bids
        #TODO 有问题.
        db.Book.remove({'bid':b['bid']})

if __name__ == "__main__":
    rm_nullcontent()
