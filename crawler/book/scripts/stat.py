#-*-coding:utf8


def stat():
    import pymongo
    connection = pymongo.Connection('localhost', 27017)
    db = connection.xiaoshuo_pict
    for b in db.Book.find():
        chapter_count = db.Chapter.find({"book_id": b['bid']}).count()
        content_count = db.Content.find({"book_id": b['bid']}).count()
        print b['title'].encode("utf-8"), chapter_count, "\t", content_count, '\t', b['image_path']
    print 'book count:', db.Book.find().count()

if __name__ == "__main__":
    stat()
