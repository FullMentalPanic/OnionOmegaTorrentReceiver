# -*- coding: utf-8 -*-
# all linux cmd used in python code
import subprocess
import os

transmission_start = ['sudo', 'service', 'transmission-daemon', 'start']
transmission_stop = ['sudo', 'service', 'transmission-daemon', 'stop']
transmission_add_torrent = ['/usr/bin/transmission-remote', "-n", "transmission:transmission", "--add"]
transmission_list = ["/usr/bin/transmission-remote -n transmission:transmission -l"]
scrapy = ['scrapy', 'crawl', 'dmhy_rss']
transmission_remove = ['/usr/bin/transmission-remote', "-n", "transmission:transmission",]
get_GPU_temp = ["/opt/vc/bin/vcgencmd measure_temp"]
disk_usage = ["df"]
HMDI_status = ["sudo tvservice -s"]
RUN_OMXPLAY_GUI = ["./omxplayer_gui"]

def Add_Torrent(url):
    transmission_add_torrent.append(url)
    return subprocess.call(transmission_add_torrent)

def List_Torrent():
    temp, err = subprocess.Popen(transmission_list, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).communicate()
    var = []
    print temp
    for line in temp.split('\n'):
        var.append(line)
    var.pop(-1)
    var.pop(-1)
    var.pop(0)
    return var

def Start_Transmission():
    subprocess.call(transmission_start)

def Stop_Transmission():
    subprocess.call(transmission_stop)

def Run_Spider():
    var = subprocess.check_output(scrapy)

def Romove_Torrent(id):
    temp = str(id)
    transmission_remove.append(temp)
    temp = '-r'
    transmission_remove.append(temp)
    subprocess.call(transmission_remove)

def Check_GPU_tempture():
    temp, err = subprocess.Popen(get_GPU_temp, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).communicate()
    return (float(temp[temp.index('=') + 1:temp.rindex("'")]))

def Check_CPU_tempture():
    try:
        tf = open('/sys/class/thermal/thermal_zone0/temp')
        temp =(float(tf.read())) / 1000
    except:
        temp = 0.0
    return temp

def check_HDD_spare():
    tmp, err = subprocess.Popen(disk_usage, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).communicate()
    for line in  tmp.split('\n'):
        if line.find('/dev/sda1') != -1:
            sda = line.split()
            spare = (float(sda[3]))/1024/1024
            return spare

'''
0x40001
Not initialized and HDMI cable is disconnected (booting without a cable)

0x40002
Not initialized but HDMI cable is connected (plugged in after boot)

0x120002
Standby (when RPi turns off the HDMI channel using tvservice -o)

0x120005
Wire disconnected (after initialization)

0x120016
Active (meaning the Pi is on the active TV input right now)
'''

def check_HDMI_status():
    tmp, err = subprocess.Popen(HMDI_status, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).communicate()
    state = tmp.split()[1]
    return state

def open_omxplay_gui():
    #RUN_OMXPLAY_GUI[0]=os.path.abspath("omplayer_gui")
    #print RUN_OMXPLAY_GUI
    #subprocess.call(RUN_OMXPLAY_GUI)
    subprocess.Popen(RUN_OMXPLAY_GUI, shell=True)
