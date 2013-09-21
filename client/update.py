# coding: utf8

import re
import json
from urlparse import urljoin
from lxml import etree

import requests

limit = 5
CRAWLER = 'xz'


def get_tasks():
    url = 'http://yiwanshu.com:8000/api/update/tasks?limit=%d' % limit
    resp = requests.get(url)
    return resp.json().get('tasks')


def is_same_chapter(chapter, latest_chapter):
    # FIXME 这里有问题
    chars = ur'[!,.()!?，。『』「」[]【】‘’“”"\'T]'
    chapter = re.sub(chars, '', chapter)
    latest_chapter = re.sub(chars, '', latest_chapter)
    try:
        c_num, chapter = chapter.split(' ', 1)
        l_num, latest_chapter = latest_chapter.split(' ', 1)
        if (c_num == l_num) or (chapter[-7:] == latest_chapter[-7:]):
            return True
    except (IndexError, ValueError):
        pass
    if chapter[-7:] == latest_chapter[-7:]:
        return True
    return False


def get_new_chapters(url, bid, chapters, latest_chapter):
    new_chapters = []
    for title, url in chapters:
        if is_same_chapter(title, latest_chapter):
            break
        else:
            new_chapters.insert(0, (title, url))
    if (len(new_chapters) == len(chapters)) and len(new_chapters) != 0:
        print ('Error: URL %s seems can not match book %s chapter %s' %
              (url, bid, latest_chapter))
    return new_chapters


def update(bid, content, title, crawler, type):
    url = 'http://yiwanshu.com:8000/api/update/%d' % int(bid)
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


def get_all_chapters(url, source_site):
    chapters = []
    resp = requests.get(url)
    content = resp.content
    tree = etree.HTML(content)
    if source_site == 'fftxt.net':
        elements = tree.xpath("//ul[@id='chapterlist']/li/a")
    elif source_site == 'hao123.se':
        elements = tree.xpath("//dl[@id='chapterlist']/dd/a")

    for ele in elements:
        if source_site == 'fftxt.net':
            chapter_url = urljoin(url, ele.attrib.get('href'))
        elif source_site == 'hao123.se':
            chapter_url = ele.attrib.get('href')
        title = ele.text
        chapters.insert(0, (title, chapter_url))
    return chapters


def get_content(url, source_site):
    resp = requests.get(url)
    html = resp.content
    tree = etree.HTML(html)
    if source_site == 'fftxt.net':
        elements = tree.xpath("//div[@class='novel_content']/text()")
        content = '<br><br>'.join(elements[1:])
    elif source_site == 'hao123.se':
        elements = tree.xpath("//div[@id='content']/text()")
        content = '<br><br>'.join(elements)
    return content


def crawl_chapters():
    print 'get update tasks from yiwanshu.com...'
    for book in get_tasks():
        bid = book.get('bid')
        source_site = book.get('source_site')
        latest_chapter = book.get('latest_chapter')
        url = book.get('source_url')
        print 'update book %s, try to visit %s' % (bid, url)
        chapters = get_all_chapters(url, source_site)
        print 'try to get new chapters.'
        new_chapters = get_new_chapters(url, bid, chapters, latest_chapter)
        if len(new_chapters) == 0:
            print 'book: %s has no new chapters\n' % bid
            continue
        for title, url in new_chapters:
            content = get_content(url, source_site)
            update(bid, content, title, CRAWLER, 'text')
            print 'update book %s, chapter %s' % (bid, title)
        print 'book %s update finish.\n\n' % bid


if __name__ == '__main__':
    crawl_chapters()
