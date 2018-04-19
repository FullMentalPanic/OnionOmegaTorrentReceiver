# -*- coding: utf-8 -*-

import imaplib2
from threading import *
from Queue import Queue
#import subprocess
import control as cl
#transmission = '/usr/bin/transmission-remote'


class Downloader(object):
    def __init__(self):
        self.thread = Thread(target=self.processor)

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
        while True:
            url = self.queue.get()
            #print url
            if url is None:
                break
            else:
                cl.Add_Torrent(url)
            self.queue.task_done()
        self.queue.task_done()
        return

    def __del__(self):
        self.stop()
        self.join()
