# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# only save new magnet
import os
import codecs
import re

class DmhyrssPipeline(object):
    def open_spider(self, spider):
        self.file = codecs.open(spider.name+ '_queue.txt','r+')
        self.torrent_list = open(spider.name+'_magnet.txt','w')
        self.queue = []

        for line in self.file:
            self.queue.append(line)

    def close_spider(self, spider):
        self.file.seek(0)
        for magnet in self.queue:
            self.file.write(magnet)
        self.file.close()
        self.torrent_list.close()

    def process_item(self, item, spider):
        title = str(item['title'].encode('utf-8'))
        location = str(item['location'].encode('utf-8'))
        magnet = str(item['magnet'].encode('utf-8'))
        self.file.seek(0)
        a = str(self.file.read())
        if a.find(title) == -1:
            if len(self.queue) < 100:
                self.queue.append(title+'\n')
            else:
                self.queue.pop(0)
                self.queue.append(title+'\n')
            self.torrent_list.write(location+','+magnet+'\n')
        else:
            pass
        return item
