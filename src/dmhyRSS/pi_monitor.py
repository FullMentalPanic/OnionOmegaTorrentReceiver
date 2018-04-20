# -*- coding: utf-8 -*-
import time
import os
import control as cl
from threading import *



class PiMonitor(object):
    def __init__(self):
        self.thread = Thread(target = self.check_harddisk_space_periodic, args = ())
        self.thread.daemon = True
              
    def run():
        self.thread.start()

    def check_harddisk_space_periodic(s = sched.scheduler(time.time, )):# every 1h =60*60 s
        while True:
            print 'check_harddisk_spare'
            time.sleep(1*60*60)

    def close(self):
        self.thread.join()

    def __del__(self):
        self.thread.join()
