#-*-coding:utf8

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def strip_special_tags(text):
    special = {
    '&nbp;': ' ', '&amp;': '&', '&quot;' : '"',
    '&lt;'   : '<', '&gt;'  : '>', 'amp;': '',
    'lt;' : '', 'gt': ''
    }
 
    for (k,v) in special.items():
        text = text.replace (k, v)
    return text

if __name__ == '__main__':
    print strip_special_tags(r'&nbp;&nbp;&nbp;&nbp;《一夜缠情：女人，要定你》　将于.13800100.开始限时免费　为期3天 &nbp;&nbp;&nbp;&nbp;在充满了暧昧，浪漫气息的伦敦，那一夜，她做了一次大胆热辣的女人。 &nbp;&nbp;&nbp;&nbp;【成年了吗？】他玩味的眼神审读着她，不沾染未成年，这是他的底线。 &nbp;&nbp;&nbp;&nbp;原本以为一辈子不会再.')
