import subprocess
import error as err


transmission = '/usr/bin/transmission-remote'

def Add_Torrent(url):
    return subprocess.call([transmission, '--add', url])

def List_Torrent():
    var = subprocess.check_output([transmission, '-l'])

    print var
