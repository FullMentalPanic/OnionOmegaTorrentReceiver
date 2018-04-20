# -*- coding: utf-8 -*-

import time
import os
import control as cl
from threading import *

class WebMonitor(object):
    def __init__(self,queue = Queue()):
        self.thread = Thread(target = self.run_spider_periodic, args = ())
        self.queue = queue
        self.thread.daemon = True

    def run():
        self.thread.start()

    def run_spider_periodic(self):  #every 12 h =12*60*60 s
        while True:
            cl.Run_Spider()
            path = '/dmhy_rss_magnet.txt'
            cwd = os.getcwd()+path
            if os.path.isfile(cwd):
                f = open(cwd)
                for magnet in f:
                    self.queue.put(magnet)
                f.close()
                os.remove(cwd)
            else:
                pass
            time.sleep(12*60*60)

    def close(self):
        self.thread.join()

    def __del__(self):
        self.thread.join()