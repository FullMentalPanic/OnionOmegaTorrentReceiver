# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# only save new magnet
import os

class DmhyrssPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name+ '_title.txt', 'w+')
        self.torrent_list = open(spider.name+'_magnet.txt','w')
        self.queue = []
        for line in self.file:
            self.queue.append(line.encode('utf8'))

    def close_spider(self, spider):
        for item in self.queue:
            self.file.write(item+'\n')
        self.file.close()
        self.torrent_list.close()

    def process_item(self, item, spider):
        title = item['title']
        magnet = item['magnet']
        if title not in self.file.read():
            if len(self.queue) < 500:
                self.queue.append(title)
            else:
                self.queue.pop(0)
                self.queue.append(title)
            self.torrent_list.write(magnet+'\n')
        else:
            pass
        return item
