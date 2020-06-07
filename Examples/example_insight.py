# -*- coding: utf8 -*-
#
#  CyKIT  2020.06.05
#  ________________________
#  example_epoc_plus.py       
#  
#  Written by Warren
#
"""

  usage:  python.exe .\example_insight.py
   
"""   
   
import os
import sys

sys.path.insert(0, '..//py3//cyUSB//cyPyWinUSB')
sys.path.insert(0, '..//py3')

import cyPyWinUSB as hid
import queue
from cyCrypto.Cipher import AES
from cyCrypto import Random

tasks = queue.Queue()

class EEG_insight(object):
    
    def __init__(self):
        self.hid = None
        self.delimiter = ", "
        self.insight_1 = [0,8,14,22,28,36,42,50,56,64,70,78,84,92,98,106,112,120,126,134,140,148,154,162,168,176,182,190,196,204,210,218,224,232,238]
        devicesUsed = 0
    
        for device in hid.find_all_hid_devices():
                if device.product_name == 'EEG Signals':
                    devicesUsed += 1
                    self.hid = device
                    self.hid.open()
                    self.serial_number = device.serial_number
                    device.set_raw_data_handler(self.dataHandler)                   
        if devicesUsed == 0:
            os._exit(0)
        sn = bytearray()
        for i in range(0,len(self.serial_number)):
            sn += bytearray([ord(self.serial_number[i])])

        # Insight Keymodel.
        k = ['\0'] * 16
        k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]

        self.key = bytes(bytearray(k))
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def dataHandler(self, data):
        join_data = ''.join(map(chr, data[1:]))
        data = self.cipher.decrypt(bytes(join_data,'latin-1')[0:32])
        tasks.put(data)

    def convertEPOC_PLUS(self, value_1, value_2):
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        return edk_value
       
    def get_data(self):
        
        try:
            data = tasks.get()
            z = ''
            packet_data = ""
            
            for i in range(1,len(data)):
                z = z + format(data[i],'08b')
            
            for i in range(2,(len(self.insight_1) ),2):
                if i == 14:
                    continue
                i_1 = self.insight_1[(i-2)]
                i_2 = self.insight_1[(i-1)]
                
                if i_2 > len(z):
                    i = len(self.insight_1)
                    continue
                
                v_1 = '0b' + z[(i_1):(i_2)]
                v_2 = '0b' + z[(i_2):(i_2+6)]
                
                packet_data = packet_data + self.convertEPOC_PLUS(str(int(eval(v_2))),str(int(eval(v_1)))) + self.delimiter
            
            packet_data = packet_data[:-len(self.delimiter)]
            return str(packet_data)
          
        except Exception as exception2:
            print(str(exception2))
      
cyHeadset = EEG_insight()
while 1:
    while tasks.empty():
        pass

    print(cyHeadset.get_data())
