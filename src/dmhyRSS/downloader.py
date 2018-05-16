# -*- coding: utf-8 -*-
#thread: download torrent from queue
from threading import *
from Queue import Queue
import control as cl
import os


class Downloader(object):
    def __init__(self,stop_event = Event()):
        self.thread = Thread(target=self.processor)
        self.thread.daemon = True
        self.stop_event = stop_event

    def start(self,):
        self.queue = Queue()
        self.thread.start()
        return self.queue

    def join(self):
        self.thread.join()

    def stop(self):
        self.queue.put(None)
        self.queue.join()

    def close(self):
        self.stop()
        self.join()

    def processor(self):
        while not self.stop_event.isSet():
            magent = self.queue.get()
            if magent is None:
                break
            else:
                url = magent[1]
                location = magent[0]
                cwd = '/mnt/volume/download/'
                #print location
                if location is not None:
                    cwd = '/mnt/volume/download/'+location+'/'
                    if not os.path.isdir(cwd):
                        cl.creat_folder(cwd)
                    else:
                        pass
                cl.Add_Torrent(url,cwd)
            self.queue.task_done()
        self.queue.task_done()
        return

    def __del__(self):
        self.stop()
        self.join()
