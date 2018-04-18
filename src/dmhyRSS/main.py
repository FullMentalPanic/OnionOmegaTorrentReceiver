from torrentreceiver import TorrentReceiver
import time
import error as err
import transmission as tran
import sys

if __name__ == '__main__':
    #try:
        a= TorrentReceiver()
        a.run()
        while True:
            #tran.List_Torrent()
            a.spider()
            time.sleep(100000)
    except:
        a.close()
    finally:
        sys.exit()
    #    a.close()
