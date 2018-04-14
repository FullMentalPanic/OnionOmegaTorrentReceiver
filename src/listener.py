import imaplib2
from threading import *
from Queue import Queue
import email

debug=1

class Listener(object):
    def __init__(self, queue = Queue(), white_list = []):
        self.thread = Thread(target=self.listening)
        self.event = Event()
        self.queue = queue
        self.white_list = white_list

    def login(self,imp4ssl,port,account,pwd):
        M = imaplib2.IMAP4_SSL(imp4ssl,int(port))
        M.login(account,pwd)
        M.select("INBOX")
        return M

    def start(self, imp4ssl, port, account, pwd):
        self.M = self.login(imp4ssl, port, account, pwd)
        self.thread.start()

    def stop(self):
        self.event.set()

    def join(self):
        self.thread.join()

    def listening(self):
        # Starting an unending loop here
        while True:
            if self.event.isSet():
                return
            self.needsync = False
            # A callback method that gets called when serve call
            # (email arrives, search, fetch).
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. This returns immediately,
            # since it's asynchronous.
            self.M.idle(callback=callback)
            self.event.wait()
            if self.needsync:
                self.pendingwork()
                self.event.clear()

    def extract_url(self, msg_num):
        typ, data = self.M.fetch(msg_num, '(RFC822)')
        body = None
        for response_part in data:
            if isinstance(response_part,tuple):
                msg = email.message_from_string(response_part[1])
                if msg['from'] not in self.white_list:
                    #print msg['subject']
                    print msg['from']
                    break

                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get('Content-Disposition'))
                        if ctype == 'text/plain' and 'attachment' not in cdispo:
                            body = part.get_payload(decode=True)  # decode
                            break
                else:
                    body = msg.get_payload()

                break
        return body

    def pendingwork(self):
        status, response = self.M.search(None, 'UNSEEN')
        unread_msg_nums = response[0].split()
        if unread_msg_nums is not None:
            for msg_num in unread_msg_nums:
                url= self.extract_url(msg_num)
                if url is not None:
                    self.queue.put(url)
                else:
                    continue

    def close(self):
        self.stop()
        self.join()
        self.M.close()
        self.M.logout()


    def __del__(self):
        self.stop()
        self.join()
        self.M.close()
        self.M.logout()
