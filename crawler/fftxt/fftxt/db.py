#-*-coding:utf-8
from pymongo import MongoClient


client = ""


def get_conn(coll_name):
    dbname = "xiaoshuo_fftxt"
    global client
    if not client:
        client = MongoClient("localhost", 27017)
    mongo_conn = client[dbname][coll_name]
    return mongo_conn

if __name__ == "__main__":
    print get_conn("book").find({"id": "2982"}).count()
