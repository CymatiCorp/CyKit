# -*- coding: utf8 -*-

#
#  CyKIT  2020.06.05
#  ________________________
#  example_epoc_x_macos.py       
#  
#  Written by zer0-pole
#
"""
  usage:  python Examples/example_epoc_x_macos.py
  
  tested on macOS 12.5
  Python 3.9.5
  pip install pycryptodome hidapi
"""

import os
import signal

import hid
from Crypto.Cipher import AES


class EEG(object):
    
    def __init__(self):
        self.hid = hid.device()
        self.delimiter = ", "
        self.cipher = None
        
        devicesUsed = 0
    
        for device in hid.enumerate():
                if device['manufacturer_string'] == 'Emotiv':
                    devicesUsed += 1
                    try :
                        self.hid.open(device['vendor_id'], device['product_id'], device['serial_number'])
                    except Exception as e:
                        if str(e) != "already open":
                            self.hid.close()
                            os._exit(0)
                    self.serial_number = device['serial_number']     

        if devicesUsed == 0:
            os._exit(0)

        serial = self.serial_number

        print("serial: ", serial)
        
        sn = bytearray()
        for i in range(0,len(serial)):
            sn += bytearray([ord(serial[i])])
        
        k = [sn[-1],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1],sn[-2],sn[-4],sn[-1],sn[-4],sn[-3],sn[-2],sn[-1],sn[-2],sn[-2],sn[-3]]

        self.cipher = AES.new(bytearray(k), AES.MODE_ECB)

    def convertEPOC_PLUS(self, value_1, value_2):
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        return edk_value

    def get_data(self, data):

        data = [el ^ 0x55 for el in data]
        data = self.cipher.decrypt(bytearray(data))

        try:
            packet_data = ""
            for i in range(2,16,2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            for i in range(18,len(data),2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            packet_data = packet_data[:-len(self.delimiter)]
            return str(packet_data)

        except Exception as exception2:
            print(str(exception2))

cyHeadset = EEG()


def handler(signum, frame):
    exit(0)

signal.signal(signal.SIGINT, handler)

while 1:
    data = cyHeadset.hid.read(32)
    print(cyHeadset.get_data(data))
