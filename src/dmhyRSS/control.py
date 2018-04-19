# -*- coding: utf-8 -*-

import subprocess
import error as err


transmission = '/usr/bin/transmission-remote'
transmission_start = ['sudo', 'service', 'transmission-daemon', 'start']
transmission_stop = ['sudo', 'service', 'transmission-daemon', 'stop']
transmission_add_torrent = [transmission, "-n", "transmission:transmission", "--add"]
transmission_list = ["/usr/bin/transmission-remote -n transmission:transmission -l"]
scrapy = ['scrapy', 'crawl', 'dmhy_rss']
transmission_remove = [transmission, "-n", "transmission:transmission",]

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
