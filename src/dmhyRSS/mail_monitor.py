# -*- coding: utf-8 -*-

#thread: check email and get magnet from inbox

import imaplib
from threading import *
from queue import Queue
import email
import time

class MailMonitor(object):
    def __init__(self, queue = Queue(), white_list = [], imp4ssl=None, port=None, account=None, pwd=None,stop_event = Event()):
        self.thread = Thread(target=self.listening, args =(imp4ssl,port,account,pwd))
        self.queue = queue
        self.white_list = white_list
        self.thread.daemon = True
        self.stop_event = stop_event

    def login(self,imp4ssl,port,account,pwd):
        self.M = imaplib.IMAP4_SSL(imp4ssl,int(port))
        self.M.login(account,pwd)
        self.M.select("INBOX")

    def logout(self):
        self.M.close()
        self.M.logout()

    def start(self):
        self.thread.start()

    def listening(self,imp4ssl,port,account,pwd):
        while not self.stop_event.isSet():
            try:
                self.login(imp4ssl, port, account, pwd)
                self.check_unread()
                self.logout()
            except:
                print ("can not read email")
            time.sleep(15 *60)

    def extract_magnet(self, msg_num):
        typ, data = self.M.fetch(msg_num, '(RFC822)')
        body = None
        subject = None
        #print (data)
        for response_part in data:
            if isinstance(response_part,tuple):
                #print (response_part)
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                #print (msg)
                subject, encoding = email.header.decode_header(msg['subject'])[0]
                #subject = msg['subject']
                subject = subject.decode('utf-8')
                #print (subject)
                if msg['from'] not in self.white_list:
                    print (msg['from'])
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
                #print (body)
                break
                

        return [subject,body]

    def check_unread(self):
        status, response = self.M.search(None, 'UNSEEN')
        unread_msg_nums = response[0].split()
        if unread_msg_nums is not None:
            for msg_num in unread_msg_nums:
                magnet= self.extract_magnet(msg_num)
                if magnet[1] is not None:
                    self.queue.put(magnet)
                else:
                    continue

    def close(self):
        self.thread.join()

    def __del__(self):
        self.thread.join()
        self.M.close()
        self.M.logout()
