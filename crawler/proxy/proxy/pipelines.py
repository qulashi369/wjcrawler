# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import re
import os
import urllib
import time
import exceptions
import socket

from scrapy.exceptions import DropItem

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProxyPipeline(object):
    def process_item(self, item, spider):
        port = item['port']
        port_re = re.compile('\d{1,5}')
        ports   = port_re.findall(port)
        if len(ports) == 0:
            raise DropItem("can not find port in %s" % item['port'])
        else:
            item['port'] = ports[0]
        #profiling the proxy
        #detect_service_url = 'http://xxx.xxx.xxx.xxx:pppp/apps/proxydetect.php'
        detect_service_url = 'http://lvyaojia.sinaapp.com/a.php'
        local_ip           = '124.205.66.195'
        proxy_  = str('http://%s:%s' % (str(item['address']), str(item['port'])))
        proxies = {'http':proxy_}
        begin_time = time.time()
        timeout = 3
        socket.setdefaulttimeout(timeout)
        try:
            data  = urllib.urlopen(detect_service_url, proxies=proxies).read()
        except exceptions.IOError:
            raise DropItem("curl download the proxy %s:%s is bad" % (item['address'],str(item['port'])))

        end_time   = time.time()
        if '' == data.strip():
            raise DropItem("data is null the proxy %s:%s is bad" % (item['address'],str(item['port'])))
        if data.find('PROXYDETECTATION') == -1:
            raise DropItem("wrong response the proxy %s:%s is bad" % (item['address'],str(item['port'])))
        if data.find('PROXYDETECTATION') != -1:
            if data.find(local_ip) == -1:
                item['type'] = 'anonymity'
            else:
                item['type'] = 'nonanonymity'
            item['delay'] = str(end_time - begin_time)
        item['timestamp'] = time.strftime('%Y-%m-%d',time.localtime(time.time()))

        #record the item info
        fp   = open(os.path.join(project_dir, 'proxies.txt'),'a')
        line = str(item['timestamp']) + '\t' + str(item['address']) + '\t' + str(item['port']) + '\t' + item['type'] + '\t' + str(item['delay']) + '\n'
        fp.write(line)
        fp.close()
        return item
