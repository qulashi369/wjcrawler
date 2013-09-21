#-*-coding:utf8

def rm_nullcontent():
    '''删除没有内容的章节和书'''
    import pymongo
    connection=pymongo.Connection('localhost',27017)
    db = connection.xiaoshuo3
    bs = []
    for b in db.Book.find():
        content_count = db.Content.find({'book_id':b['bid']}).count()
        if content_count == 0:
            print "正在删除 ", b['title']
            db.Chapter.remove({'book_id':b['bid']})
            db.Content.remove({'book_id':b['bid']})
            bs.append(b['title'])
    for bt in bs:
        #TODO 有问题.
        db.Book.remove({'title':bt})

if __name__ == "__main__":
    rm_nullcontent()
