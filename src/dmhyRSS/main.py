# -*- coding: utf-8 -*-

from torrent_collect import TorrentCollect
import time
import sys
from pi_monitor import PiMonitor

if __name__ == '__main__':
    #try:
        a= TorrentCollect()
        a.run()
        pi = PiMonitor()
        pi.check_Pi_State_periodic()
        #while True:
        #    time.sleep(100000)
    #except:
        a.close()
    #finally:
        sys.exit()
