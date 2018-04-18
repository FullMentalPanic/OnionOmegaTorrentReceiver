from listener import Listener
from downloader import Downloader
import yaml
import error as err
import subprocess
import time
import os
from pathlib import Path


class TorrentReceiver(object):
    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        self.mail = cfg['email']

    def run(self):
        self.Worker = Downloader()
        self.Workqueue = self.Worker.start()
        self.Receiver = Listener(self.Workqueue, self.mail['white_list'])
        self.Receiver.start(self.mail['imp4ssl'], self.mail['port'], self.mail['account'], self.mail['password'])

    def spider(self):
        subprocess.check_output(['scrapy', 'crawl', 'dmhy_rss'])
        path = '/dmhy_rss_magnet.txt'
        cwd = os.getcwd()+path
        #print cwd

        if Path(cwd).exists():
            #print "to do list"
            f = open(cwd)
            for magnet in f:
                self.Workqueue.put(magnet)
            f.close()
            os.remove(cwd)
        else:
            #print " no to do list"
            pass


    def close(self):
        self.Receiver.close()
        self.Worker.close()


    def __del__(self):
        self.Receiver.close()
        self.Worker.close()
