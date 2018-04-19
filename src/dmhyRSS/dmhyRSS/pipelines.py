# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import os

class DmhyrssPipeline(object):
    def open_spider(self, spider):
        self.file = open(spider.name+ '_title.txt', 'w+')
        self.torrent_list = open(spider.name+'_magnet.txt','w')
        self.queue = []
        for line in self.file:
        #if os.stat(spider.name+ '_title.json').st_size == 0:
            self.queue.append(line.encode('utf8'))
        #else:
        #self.queue = json.load(self.file)
        #    print queue


    def close_spider(self, spider):
        #self.file.write('{'+'\n')
        for item in self.queue:
            self.file.write(item+'\n')
        self.file.close()
        self.torrent_list.close()

    def process_item(self, item, spider):
        title = item['title']
        magnet = item['magnet']
        #title = json.dumps(item['title'])
        #title = str(title)
        #need to dump to json for title
        #print self.queue
        #print len(self.queue)
        #if title not in self.queue:
        if title in self.file.read():
            #print 'find'
            if len(self.queue) < 200:
                self.queue.append(title)
            else:
                self.queue.pop(0)
                self.queue.append(title)
            self.torrent_list.write(magnet+'\n')
        else:
            pass
        return item
