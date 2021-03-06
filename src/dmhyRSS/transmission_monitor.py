# -*- coding: utf-8 -*-
# thread: clear finish job from transmission
import time
import os
import control as cl
from threading import *

class TransmissionMonitor(object):
    def __init__(self, stop_event = Event()):
        self.thread = Thread(target = self.remove_transmission_finish_work_periodic, args = ())
        self.thread.daemon = True
        self.stop_event = stop_event

    def start(self):
        self.thread.start()

    def remove_transmission_finish_work_periodic(self): # every 4h  = 4*60 *60
        while not self.stop_event.isSet():
            check_list =  cl.List_Torrent()
            if not check_list:
                pass
            else:
                ID ='-t'
                for item in check_list:
                    #print (temp)
                    temp = item.split()
                    if temp[4] == 'Done':
                        ID = ID+temp[0]+','
                    else:
                        pass
                if ID != '-t':
                    cl.Romove_Torrent(ID)
                else:
                    pass
            time.sleep(4*60*60)


    def close(self):
        self.thread.join()

    def __del__(self):
        self.thread.join()
