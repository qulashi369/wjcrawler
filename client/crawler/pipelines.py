
class ContentPipeline(object):

    def process_item(self, item, spider):
        bid = item['bid']
        content = item['content']
        title = item['title']
        type = item['type']
        crawler = item['crawler']

        url = 'http://localhost:8000/api/update/%d' % int(bid)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = dict(
            crawler=crawler,
            chapter={
                'type': type,
                'title': title,
                'content': content
            }
        )
        data = json.dumps(data)
        resp = requests.post(url, data, headers=headers)
        assert resp.status_code == 200, 'HTTP ERROR!!'
        return item
