# -*- coding: utf-8 -*-
#thread: run scray and put last magent to queue
import time
import os
import control as cl
from threading import *
from queue import Queue

class WebMonitor(object):
    def __init__(self,queue = Queue(),stop_event = Event()):
        self.thread = Thread(target = self.run_spider_periodic, args = ())
        self.queue = queue
        self.thread.daemon = True
        self.stop_event = stop_event

    def start(self):
        self.thread.start()

    def run_spider_periodic(self):  #every 12 h =12*60*60 s
        while not self.stop_event.isSet():
            cl.Run_Spider()
            path = '/dmhy_rss_magnet.txt'
            cwd = os.getcwd()+path
            if os.path.isfile(cwd):
                f = open(cwd)
                for magnet in f:
                    #magnet = magnet.decode('utf-8')
                    tmp = magnet.split(',')
                    self.queue.put(tmp)
                f.close()
                os.remove(cwd)
            else:
                pass
            time.sleep(12*60*60)

    def close(self):
        self.thread.join()

    def __del__(self):
        self.thread.join()
