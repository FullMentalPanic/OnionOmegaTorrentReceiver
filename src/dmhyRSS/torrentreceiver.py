# -*- coding: utf-8 -*-

from listener import Listener
from downloader import Downloader
import yaml
import error as err
import subprocess
import time
import os
import control as cl
import sched, time



class TorrentReceiver(object):
    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        self.mail = cfg['email']

    def monitor(self):
        s = sched.scheduler(time.time, time.sleep)

        def run_spider_periodic( s = sched.scheduler(time.time, time.sleep) ): #priority 7 #every 12 h =12*60*60 s
            s.enter(12*60*60, 7, run_spider_periodic, (s))

            cl.Run_Spider()
            path = '/dmhy_rss_magnet.txt'
            cwd = os.getcwd()+path
            if os.path.isfile(cwd):
                f = open(cwd)
                for magnet in f:
                    self.Workqueue.put(magnet)
                f.close()
                os.remove(cwd)
            else:
                pass



        def remove_transmission_finish_work_periodic(s = sched.scheduler(time.time, time.sleep)): #priority 6 every 4h  = 4*60 *60
            s.enter(4*60*60, 6, remove_transmission_finish_work_periodic, (s))

            check_list =  cl.List_Torrent()
            if not check_list:
                pass
            else:
                ID ='-t'
                for item in check_list:
                    temp = item.split()
                    if temp[4] == 'Done':
                        ID = ID+temp[0]+','
                    else:
                        pass
                if ID != '-t':
                    cl.Romove_Torrent(ID)
                else:
                    pass


        def check_harddisk_space_periodic(s = sched.scheduler(time.time, time.sleep)):#priority 5  every 1h =60*60 s
            s.enter(1*60*60, 6, check_harddisk_space_periodic, (s))
            print 'check_harddisk_spare'

        check_harddisk_space_periodic()
        remove_transmission_finish_work_periodic()
        run_spider_periodic()
        s.run()

    def run(self):
        self.Worker = Downloader()
        self.Workqueue = self.Worker.start()
        self.Receiver = Listener(self.Workqueue, self.mail['white_list'])
        self.Receiver.start(self.mail['imp4ssl'], self.mail['port'], self.mail['account'], self.mail['password'])
        self.monitor()




    def close(self):
        self.Receiver.close()
        self.Worker.close()


    def __del__(self):
        self.Receiver.close()
        self.Worker.close()
