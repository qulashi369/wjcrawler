#!/usr/bin/env python

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
import json
import pymongo

users = {"yj": "yj"}
client = ''


def mongo(db, coll):
    global client
    if not client:
        client = pymongo.MongoClient("localhost", 27017)
    return client[db][coll]


class Echo(Protocol):

    def dataReceived(self, data):
        """
        As soon as any data is received, write it back.
        """
        try:
            data = json.loads(data)
            if data['name'] in users:
                print data
                self.dbconn = mongo('xiaoshuo5', data['coll'])
                self.dbconn.save(data)
        except:
            pass


def main():
    f = Factory()
    f.protocol = Echo
    reactor.listenTCP(9000, f)
    reactor.run()

if __name__ == '__main__':
    main()
