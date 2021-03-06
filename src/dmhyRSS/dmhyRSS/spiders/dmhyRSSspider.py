## -*- coding: utf-8 -*-
# get magnet from target web
import scrapy
from dmhyRSS.items import *
import yaml
import re

class dmhyRSSspider(scrapy.Spider):
    name = "dmhy_rss"
    start_urls = [
        'https://share.dmhy.org/topics/rss/rss.xml',
    ]

    def parse(self, response):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        my_spider = cfg['re_spider']
        re_list = my_spider['dmhy_rss']
        location = my_spider['location']
        item = DmhyrssItem()
        for rss in response.xpath("//item"):
            title = rss.xpath(".//title/text()").extract_first()
            count = 0
            for re_rule in re_list:
                if re.search(re_rule, title) is not None:
                    item['title'] = title
                    item['location'] = location[count]
                    item['magnet'] = rss.xpath(".//enclosure/@url").extract_first()
                    yield item
                else:
                    pass
                count = count + 1
