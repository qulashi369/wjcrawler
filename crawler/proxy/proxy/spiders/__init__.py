# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from proxy.items import ProxyItem
import re

class ProxycrawlerSpider(CrawlSpider):
    name = 'proxy'
    allowed_domains = ['www.cnproxy.com']
    indexes    = [1,2,3,4,5,6,7,8,9,10]
    start_urls = []
    for i in indexes:
        url = 'http://www.cnproxy.com/proxy%s.html' % i
        start_urls.append(url)
    start_urls.append('http://www.cnproxy.com/proxyedu1.html')
    start_urls.append('http://www.cnproxy.com/proxyedu2.html')

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        addresses = hxs.select('//tr[position()>1]/td[position()=1]').re('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        protocols = hxs.select('//tr[position()>1]/td[position()=2]').re('<td>(.*)<\/td>')
        locations = hxs.select('//tr[position()>1]/td[position()=4]').re('<td>(.*)<\/td>')
        ports_re  = re.compile('write\(":"(.*)\)')
        raw_ports = ports_re.findall(response.body);
        port_map = {'v':'3','m':'4','a':'2','l':'9','q':'0','b':'5','i':'7','w':'6','r':'8','c':'1','+':''}
        ports     = []
        for port in raw_ports:
            tmp = port
            for key in port_map:
                tmp = tmp.replace(key, port_map[key]);
            ports.append(tmp)
        items = []
        for i in range(len(addresses)):
            try:
                item = ProxyItem()
                item['address']  = addresses[i]
                item['protocol'] = protocols[i]
                item['location'] = locations[i]
                item['port']     = ports[i]
                items.append(item)
            except IndexError:
                continue
        return items

