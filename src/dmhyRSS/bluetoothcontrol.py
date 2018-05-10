# -*- coding: utf-8 -*-
#thread: bluetooth control sim keyborad input
from threading import *
import control as cl
from bluetooth import *
import time


class BluetoothControl(object):
    def __init__(self):
        self.thread = Thread(target=self.bluetoothhost)
        self.thread.daemon = True

    def start(self,):
        self.SetUpbluetoothhost()
        self.thread.start()

    def join(self):
        self.thread.join()


    def SetUpbluetoothhost(self):
        self.server_sock=BluetoothSocket(RFCOMM )
        self.server_sock.bind(("",PORT_ANY))
        self.server_sock.listen(1)
        port = self.server_sock.getsockname()[1]
        #uuid = "0000111f-0000-1000-8000-00805f9b34fb"
        #advertise_service( self.server_sock, "Service", uuid )
        uuid = "00001101-0000-1000-8000-00805F9B34FB"

        advertise_service( self.server_sock, "AquaPiServer",service_id = uuid,service_classes = [ uuid, SERIAL_PORT_CLASS ],profiles = [ SERIAL_PORT_PROFILE ],)


    def bluetoothhost(self):
        #Nexus 5
        #Device 2C:54:CF:73:60:CF UUIDs: 0000111f-0000-1000-8000-00805f9b34fb
        #Wait_Bluetooth_Pairing()
        (self.client_sock,address) = self.server_sock.accept()
        print("Accepted connection from ", address)
        try:
            while True:
                data = self.client_sock.recv(4)
                print "recv data %s", data
                if data == "n\n":
                    cl.simluate_input('Up')
                elif data == "l\n":
                    cl.simluate_input('Down')
                elif data == "o\n":
                    cl.simluate_input('Return')
                elif data == "s\n":
                    cl.simluate_input('ctrl+q')
                elif data == "p\n":
                    cl.simluate_input('ctrl+p')
                elif data == "f\n":
                    cl.simluate_input('Right')
                elif data == "b\n":
                    cl.simluate_input('Left')
                elif data == "e\n":
                    cl.simluate_input('ctrl+e')
                else:
                    continue
        except IOError:
            pass
        else:
            self.client_sock.close()

    def close(self):
        self.server_sock.close()
        self.join()

    def __del__(self):
        self.server_sock.close()
        self.join()


if __name__ == '__test__':
    app = BluetoothControl()
    app.start()
    while True:
        time.sleep(10)
