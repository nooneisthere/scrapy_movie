# -*- coding: utf-8 -*-
import scrapy
from scrapy1.myutility import urlHelper
import os,sys

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo'
    allowed_domains = ['dxsxs.com']
    start_urls = ['http://www.dxsxs.com/waiwen/2105']
    domain = 'http://www.dxsxs.com'
    log = open("xiaoshuo.txt", mode='a',encoding='utf-8')

    def parse(self, response):
        atitle = response.css('div.atitle h2::text').get()
        if (atitle):
            self.log.writelines(atitle)
            zw = response.css('div.zw *::text').getall()
            print(atitle)
            self.log.writelines(zw)

        else:
            infos = response.css('#yuedu a')
            for link in infos:
                href = link.css('::attr(href)').get()
                print( urlHelper.getURI(response.url) )
                url = urlHelper.makeURL(href, self.domain)
                print(link.css('::text').get(), '   => ' ,url)
                self.log.writelines(url + ' => ' +link.css('::text').get() + '\n')
                yield scrapy.Request(url=url, callback=self.parse)

