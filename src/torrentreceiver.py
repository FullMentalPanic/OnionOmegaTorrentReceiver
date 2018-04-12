from listener import Listener
from downloader import Downloader
import imaplib2
import time
import yaml

class TorrentReceiver(object):
    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        self.mail = cfg['email']

    def login(self,imp4ssl,port,account,pwd):
        M = imaplib2.IMAP4_SSL(imp4ssl,int(port))
        M.login(account,pwd)
        M.select("INBOX")
        return M

    def run(self):
        M = self.login(self.mail['imp4ssl'], self.mail['port'], self.mail['account'], self.mail['password'])
        self.worker = Downloader()
        self.workqueue = self.worker.start()
        self.Receiver = Listener(self.workqueue, self.mail['white_list'])
        self.Receiver.start(M)

    def close(self):
        self.Receiver.close()
        self.worker.close()
        self.M.close()
        self.M.logout()

    def __del__(self):
        self.Receiver.close()
        self.worker.close()
        self.M.close()
        self.M.logout()


if __name__ == '__main__':
    try:
        a= TorrentReceiver()
        a.run()
        while True:
            time.sleep(10)
    except:
        a.close()
    finally:
        a.close()
