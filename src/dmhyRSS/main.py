# -*- coding: utf-8 -*-

from torrentreceiver import TorrentReceiver
import time
import sys

if __name__ == '__main__':
    try:
        a= TorrentReceiver()
        a.run()
        while True:
            time.sleep(100000)
    except:
        a.close()
    finally:
        sys.exit()
