# -*- coding: utf8 -*-
#
#  CyKIT 3.3  2020.06.05
#  ________________________
#  example_epoc_plus.py       
#  
#  Written by Warren and CMETAHA
#
"""
   
  usage:  python.exe .\example2_epoc_plus.py
   
  ( May need to adjust the key below, based on whether 
    device is in 14-bit mode or 16-bit mode. )
  
"""

import os
import sys
sys.path.insert(0, './cyPyWinUSB')
import cyPyWinUSB as hid
import queue
from cyCrypto.Cipher import AES
from cyCrypto import Random
import signal
import time

tasks = queue.Queue()
running = True
end_timestamp = 0

def signal_handler(sig, frame):
    global running
    global end_timestamp
    if end_timestamp != 0:
        print("force stop")
        os.exit(0)
    end_timestamp = time.time_ns()
    print("stoped at: ", end_timestamp)

    running = False

signal.signal(signal.SIGINT, signal_handler)

class EEG(object):
    
    def __init__(self):
        self.hid = None
        self.delimiter = ", "
        
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
        sn = self.serial_number
        
        # EPOC+ in 16-bit Mode.
        k = ['\0'] * 16
        k = [sn[-1],sn[-2],sn[-2],sn[-3],sn[-3],sn[-3],sn[-2],sn[-4],sn[-1],sn[-4],sn[-2],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1]]
        
        # EPOC+ in 14-bit Mode.
        #k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]
        
        self.key = str(''.join(k))
        self.cipher = AES.new(self.key.encode("utf8"), AES.MODE_ECB)

    def dataHandler(self, data):
        try:
            tasks.put((data[1:], time.time_ns()))
        except Exception as exception2:
            print(str(exception2))

    def convertEPOC_PLUS(self, value_1, value_2):
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        return edk_value
       
    def get_data(self):
        try:
            raw_data, timestamp = tasks.get()
            # print(str(data[0])) COUNTER
            join_data = ''.join(map(chr, raw_data))
            data = self.cipher.decrypt(bytes(join_data, 'latin-1')[0:32])
            if str(data[1]) == "32":  # No Gyro Data.
                print("gyro data")
                return

            #counter
            packet_data = str(data[0]) + self.delimiter
            for i in range(2,16,2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            for i in range(18,len(data),2):
                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

            return packet_data, timestamp

        except Exception as exception2:
            print(str(exception2))


if len(sys.argv) != 2:
    print('Provide only output file name as arg')
    sys.exit(0)
file_name = sys.argv[1] + ".csv"

if os.path.exists(file_name):
    print("file already exists")
    os.exit(0)
    
start_timestamp = time.time_ns()
cyHeadset = EEG()
print("started at: ", start_timestamp)

while running:
    time.sleep(0.1)
    continue

last_timestamp = start_timestamp
try:
    print("writing file: ", file_name)
    f = open(file_name, 'w')
    while last_timestamp <= end_timestamp:

        data_str, last_timestamp = cyHeadset.get_data()
        f.write(data_str + str(last_timestamp) + '\n')
    f.flush()
    os.fsync(f.fileno())
    f.close()
except Exception as msg:
    print(str(msg))
