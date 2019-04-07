# -*- coding: utf-8 -*-
import scrapy
import random, time, re
from scrapy1.items import Scrapy1Item

class MovieSpider(scrapy.Spider):

    name = 'movie'
    allowed_domains = ['dysfz.tv']

    mystate = {}
    domain = 'https://www.dysfz.tv'

    '''
    common_url = (
        'https://www.dysfz.tv/',
        'https://www.dysfz.tv/tv/',
        'https://www.dysfz.tv/discuss/',
        'https://www.dysfz.tv/hot/',
        'https://www.dysfz.tv/cartoon/',
        'https://www.dysfz.tv/news/',
        'https://www.dysfz.tv/user/login.php',
        'https://www.dysfz.tv/user/reg.php',
        'https://www.dysfz.tv/movie23645.html')
    '''
    def start_requests(self):
        start = 1
        last_uri = self.getstate('last_uri')
        if last_uri:
            print('__________________________last_uri: ', last_uri)
            start = int(last_uri[6:])

        #now they 2019/02/21 they have about 1290 pages for /movie/xxx
        for i in range(start,1300):
            start_url = 'https://www.dysfz.tv/movie/'+str(i)

            yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        infos = response.css('div.detail p a')
        item = Scrapy1Item()
        uri = getURI(response.url)
        title = response.css('title::text').get()
        print ('!!!!!!!!!!', uri)

        #detailed download page, otherwise it is index page
        if (infos):
            #print ('1111111111111111',infos.get())
            for link in infos:
                href = link.css('::attr(href)').get()
                #print ('333333333333333333333333',pinfo, link.get())

                if not href:
                    print(r'---------nohref => ', link.get())
                elif validSource(href) :
                    if validSource(href) == 'pan':
                        #because pan.baidu usually need extra password info, ./.. to get parent node
                        href = link.xpath('./..').get()
                        #print('444444444444444444',href )

                    refer = self.getstate(uri)
                    if refer:
                        item['title'] = refer['title']
                        item['dbscore'] = refer['dbscore']

                    else:
                        print('555555555555555555 no refer uri ',uri )
                        item['title'] = title[:20]

                    item['fname'] = link.css('::text').get()
                    item['url'] = href
                    item['refer'] = uri
                    yield item

            self.delstate(uri)
        else:
            print('----------------here------------', uri )
            self.setstate('last_uri', uri)
            time.sleep(3)

            #index page
            for li in response.css('ul.movie-list li'):

                #may need another loop to get valid <a>
                link = li.css('a')
                url = link.css('a::attr(href)').get()
                dbscore = li.css('.dbscore b::text').get()
                if not url:
                    print(r'!!!#no href => ', link.get())

                elif url and url.startswith(self.domain + '/movie'):
                    url = makeURL(url, self.domain)
                    text = link.css('::text').get()
                    if not text :
                         print('nonononotext', ' => ', link.get)

                    #pass
                    #delay hanle by setting.py
                    #if not url in self.common_url:
                    #    time.sleep(random.random()*3)
                    else:
                        self.setstate(getURI(url),{'title':text,'dbscore':dbscore})

                        yield scrapy.Request(url=url, callback=self.parse)

    def getstate(self, thekey):
        if (hasattr(self, 'state') and thekey in self.state):
            return self.state[thekey]

    def delstate(self, thekey):
        if (hasattr(self, 'state') and thekey in self.state):
            del self.state[thekey]

    def setstate(self, thekey,thevalue):
        if hasattr(self, 'state') :
            self.state[thekey] = thevalue


def makeURL(url, domain):
    if (url.startswith('http')):
        return url
    elif (url.startswith('/')):
        return domain + url
    elif (url.startswith('javascript')):
        return ''
    else:
        return ''

def validSource(url):
    valid = ('ed2k', 'magnet' ,'thunder')
    for st in valid:
        if url.startswith(st): return st

    for st in ('http://pan.', 'https://pan.'):
        if url.startswith(st): return 'pan'

def getURI(url):
    match=re.match(r'^http[s]?://.+?/(.+)$',url)
    if match:
        return match.group(1)



