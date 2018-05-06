# -*- coding: utf-8 -*-
# all linux cmd used in python code
import subprocess
import os

def Add_Torrent(url,location):
    transmission_add_torrent = ['/usr/bin/transmission-remote', "-n", "transmission:transmission",]

    transmission_add_torrent.append("--add")
    transmission_add_torrent.append(url)
    transmission_add_torrent.append("-w")
    transmission_add_torrent.append(location)
    return subprocess.call(transmission_add_torrent)

def List_Torrent():
    transmission_list = ["/usr/bin/transmission-remote -n transmission:transmission -l"]
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
    transmission_start = ['sudo', 'service', 'transmission-daemon', 'start']
    subprocess.call(transmission_start)

def Stop_Transmission():
    transmission_stop = ['sudo', 'service', 'transmission-daemon', 'stop']
    subprocess.call(transmission_stop)

def Run_Spider():
    scrapy = ['scrapy', 'crawl', 'dmhy_rss']
    var = subprocess.check_output(scrapy)

def Romove_Torrent(id):
    transmission_remove = ['/usr/bin/transmission-remote', "-n", "transmission:transmission",]
    temp = str(id)
    transmission_remove.append(temp)
    temp = '-r'
    transmission_remove.append(temp)
    subprocess.call(transmission_remove)

def Check_GPU_tempture():
    get_GPU_temp = ["/opt/vc/bin/vcgencmd measure_temp"]
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
    disk_usage = ["df"]
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
    HMDI_status = ["sudo tvservice -s"]
    tmp, err = subprocess.Popen(HMDI_status, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True).communicate()
    state = tmp.split()[1]
    return state

def open_omxplay_gui():
    RUN_OMXPLAY_GUI = ["./omxplayer_gui"]
    subprocess.Popen(RUN_OMXPLAY_GUI, shell=True)

def simluate_input(opertion):
    KEY_INPUT = ['xdotool', 'key']
    KEY_INPUT.append(opertion)
    subprocess.call(KEY_INPUT)

def creat_folder(dir):
    subprocess.call(['mkdir',dir])
    subprocess.call(['sudo','chmod', '-R', '777', dir])

def Bluetooth_Discoverable():
    subprocess.call(['sudo','hciconfig','hci0','up'])
    #subprocess.call(['sudo','hciconfig','hci0','sspmode','1'])
    subprocess.call(['sudo','hciconfig','hci0','piscan'])
