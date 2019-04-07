# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
import random, time

class JianshuSpider(scrapy.Spider):
    name = 'jianshu'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/zhaopin/Python/1/?filterOption=1',
                ]
    domain = 'https://www.lagou.com'

    def parse(self, response):
        htmldom = BeautifulSoup(response.body, 'html.parser')
        infos = htmldom.find_all('li','con_list_item default_list')
        for info in  infos :
            print(info.attrs['data-positionname'],\
                info.attrs['data-salary'],\
                (info.find('span', 'format-time')).string,\
                info.find('div', 'li_b_l').get_text().split('/')[-1],\
                info.attrs['data-company'])

        for link in htmldom('a'):
            url = makeURL(link.attrs['href'], self.domain)
            if url :
                time.sleep(random.random()*3)
                print(link.string, ' => ', url)
                yield scrapy.Request(url=url, callback=self.parse)


def makeURL(url, domain):
    if (url.startswith('http')):
        return url;
    elif (url.startswith('/')):
        return domain + url
    elif (url.startswith('javascript')):
        return ''
    else:
        return ''


