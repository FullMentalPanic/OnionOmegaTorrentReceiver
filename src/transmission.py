import subprocess
import error as err


transmission = '/usr/bin/transmission-remote'
transmission_start = ['sudo', 'service', 'transmission-daemon', 'start']
transmission_stop = ['sudo', 'service', 'transmission-daemon', 'stop']
transmission_add_torrent = [transmission, "-n", "transmission:transmission", "--add"]
transmission_list = [transmission, "-n", "transmission:transmission", "-l"]

def Add_Torrent(url):
    transmission_add_torrent.append(url)
    return subprocess.call(transmission_add_torrent)

def List_Torrent():
    var = subprocess.check_output(transmission_list)

    print var

def Start_Transmission():
    subprocess.call(transmission_start)

def Stop_Transmission():
    subprocess.call(transmission_stop)
