#-*-coding:utf-8
from db import get_conn


class FftxtPipeline(object):
    def process_item(self, item, spider):
        conn = get_conn(item.mongoname)
        conn.save(dict(item))
