# -*- coding: utf-8 -*-
# main process : check pi state, run TorrentCollect and omxplay
import time
import os
import control as cl
import RPi.GPIO as GPIO
from threading import *

debug = 0

class PiMonitor(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3, GPIO.IN, pull_up_down = GPIO.PUD_UP) # shutdown button
        GPIO.setup(26,GPIO.OUT, initial = 1) # Fan control
        GPIO.add_event_detect(3, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)
        #GPIO.add_event_detect(15, GPIO.FALLING, callback = BluetoothOn, bouncetime = 2000)
        self.thread = Thread(target=self.moniter)
        self.thread.daemon = True
        self.thread_stop_event = Event()

    def start(self):
        self.thread_stop_event.clear()
        self.thread.start()
        return self.thread_stop_event

    def moniter(self):
        while True: # every 1m =30 s
            self.check_harddisk_spare()
            self.control_CPU_GPU_tempture()
            time.sleep(1*20)

    def check_harddisk_spare(self):
        spare = cl.check_HDD_spare()
        if debug:
            print (spare)
        if spare < 1.0:
            self.thread_stop_event.set()
        else:
            pass

    def check_HDMI_status(self):
        status = cl.check_HDMI_status()
        if debug:
            print (status)

    def control_CPU_GPU_tempture(self):
        CPU_temp = cl.Check_CPU_tempture()
        GPU_temp = cl.Check_GPU_tempture()

        if debug:
            print (CPU_temp)
            print (GPU_temp)

        if CPU_temp > 50.0 or GPU_temp >50.0:
            GPIO.output(26,0)
        elif CPU_temp < 45.0 and GPU_temp < 45.0:
            GPIO.output(26,1)
        else:
            pass
    def close(self):
        self.thread.join()

    def __del__(self):
        self.thread.join()

def Shutdown(channel):
    os.system("sudo shutdown -h now")

if __name__ == '__test__':
    try:
        app = PiMonitor()
        app.run()
    except:
        app.close()
