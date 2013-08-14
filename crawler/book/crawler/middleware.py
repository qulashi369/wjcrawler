import random


class UserAgentsMiddleware(object):
    def __init__(self, filename):
        with open(filename) as f:
            self.user_agents = [
                line.strip()
                for line in f.readlines()
            ]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get(
                'USER_AGENTS_LIST_FILE',
                'user-agents.txt'
            ),
        )

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agents)
        request.headers.setdefault('User-Agent', user_agent)


class ProxyMiddleware(object):
    def __init__(self, filename):
        self.file = filename

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler.settings.get('PROXY_LIST_FILE',),
        )

    def process_request(self, request, spider):
        fd = open(self.file, 'r')
        data = fd.readlines()
        fd.close()
        length = len(data)
        index = random.randint(0, length-1)
        item = data[index]
        arr = item.split()
        request.meta['proxy'] = 'http://%s:%s' % (arr[1], arr[2])
