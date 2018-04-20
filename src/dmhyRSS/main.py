# -*- coding: utf-8 -*-

from torrent_collect import TorrentCollect
import time
import sys

if __name__ == '__main__':
    #try:
        a= TorrentCollect()
        a.run()
        while True:
            time.sleep(100000)
    #except:
        a.close()
    #finally:
        sys.exit()
