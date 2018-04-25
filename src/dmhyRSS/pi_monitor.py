# -*- coding: utf-8 -*-
import time
import os
import control as cl
import RPi.GPIO as GPIO
#from torrent_collect import TorrentCollectRun
import torrent_collect
debug = 0
# set as main process

class PiMonitor(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP) # shutdown button
        GPIO.setup(11,GPIO.OUT, initial = 0) # Fan control
        GPIO.add_event_detect(3, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)

    def check_Pi_State_periodic(self):# every 1m =30 s

            torrent = TorrentCollect()
            torrent.run()

            while True:
                try:
                    self.check_harddisk_spare()
                    self.check_HDMI_status()
                    self.control_CPU_GPU_tempture()
                    time.sleep(1*20)
                except Exception as 'HDD space full': 
                    torrent.close()

    def check_harddisk_spare(self):
        spare = cl.check_HDD_spare()
        if debug:
            print spare
        if spare < 1.0:
            raise Exception('HDD space full')
        else:
            pass

    def check_HDMI_status(self):
        #print 'check_HDMI_state'
        status = cl.check_HDMI_status()
        if debug:
            print status

    def control_CPU_GPU_tempture(self):
        CPU_temp = cl.Check_CPU_tempture()
        GPU_temp = cl.Check_GPU_tempture()

        if debug:
            print CPU_temp
            print GPU_temp

        if CPU_temp > 50.0 or GPU_temp >50.0:
            GPIO.output(11,1)
        elif CPU_temp < 45.0 and GPU_temp < 45.0:
            GPIO.output(11,0)
        else:
            pass

def Shutdown(channel):
    os.system("sudo shutdown -h now")
