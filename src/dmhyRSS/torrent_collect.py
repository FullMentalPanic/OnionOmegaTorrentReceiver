# -*- coding: utf-8 -*-

from mail_monitor import MailMonitor
from web_monitor import WebMonitor
from pi_monitor import PiMonitor
from transmission_monitor import TransmissionMonitor
from downloader import Downloader
import yaml
import error as err
import time
import control as cl



class TorrentCollect(object):    
    def __init__(self):
        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)
        self.mail = cfg['email']

    def run(self):
        self.bt = Downloader()
        self.magnetqueue = self.bt.start()
        self.tran_checker = TransmissionMonitor()
        self.tran_checker.start()
        time.sleep(53)
        self.pi_checker = PiMonitor()
        self.pi_checker.start()
        time.sleep(53)
        self.mailreceiver = MailMonitor(self.magnetqueue, self.mail['white_list'])
        self.mailreceiver.start(self.mail['imp4ssl'], self.mail['port'], self.mail['account'], self.mail['password'])
        time.sleep(53)
        self.webreceiver = WebMonitor(self.magnetqueue)
        self.webreceiver.start()

    def close(self):
        self.webreceiver.close()
        self.mailreceiver.close()
        self.pi_checker.close()
        self.tran_checker.close()
        self.bt.close()

    def __del__(self):
        self.webreceiver.close()
        self.mailreceiver.close()
        self.pi_checker.close()
        self.tran_checker.close()
        self.bt.close()
