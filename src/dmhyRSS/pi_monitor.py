# -*- coding: utf-8 -*-
import time
import os
import control as cl
from threading import *



class PiMonitor(object):
    def __init__(self):
        self.thread = Thread(target = self.check_Pi_State_periodic, args = ())
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def check_Pi_State_periodic(self):# every 1m =60 s
        while True:
            self.check_harddisk_spare()
            self.check_HDMI_status()
            time.sleep(1*60)

    def check_harddisk_spare(self):
        print 'check_harddisk_spare'

    def check_HDMI_status(self):
        print 'check_HDMI_state'

    def close(self):
        self.thread.join()

    def __del__(self):
        self.thread.join()
