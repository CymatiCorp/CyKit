# -*- coding: utf8 -*-
#
#  CyKIT 2022.July.27
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
#  eeg.py
#  Written by Warren
#
#  Emokit Written by Cody Brocious
#  Emokit Written by Kyle Machulis
#  CyKIT  Written by Warren
#  Contributions  by Severin Lemaignan
#  Contributions  by Sharif Olorin
#  Contributions  by Bill Schumacher
#  Contributions  by CaptainSmiley
#  Contributions  by yikestone
#

import time
import os
import sys
import platform
import socket
import struct
import operator
import math
import queue
import threading
import traceback
import array
import inspect
import random 

#  Import C functions for Bluetooth.
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
from ctypes import *
from ctypes.wintypes import HANDLE, ULONG, DWORD, USHORT

#  Detect 32 / 64 Bit Architecture.
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
arch = struct.calcsize("P") * 8

#  Add a relative local path to CyKIT.
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
localPath = ((sys.argv[0]).replace('/','\\')).split('\\')
localPath = localPath[0:(len(localPath) -1)]
localPath = str('\\'.join(localPath ))
if localPath == None:
    localPath = ".\\"

sys.path.insert(0, localPath)

class dbg():
    def txt(custom_string):
        return
       
        #return
        global store_str
        global store_inc
        global dupe_msg
        mirror.text("G" + str(custom_string))
        return
        if 'dupe_msg' in globals() and dupe_msg == store_str + custom_string:
            if 'store_inc' not in globals():
                store_inc = 0 
            store_inc = store_inc + 1
            if store_inc > 20:
                store_inc = 0
            return
        
        if 'store_str' in globals():
            dupe_msg = store_str + custom_string
        
        store_str = custom_string
        #return
        try:
            print(custom_string)
            return
        except OSError as exp:
            return
           

#  Custom print class. Workaround for OSError: raw write().
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
class mirror():
    def text(custom_string):
        try:
            print(str(custom_string))
            return
        except OSError as exp:
            return
     
parameters = len(sys.argv)
if parameters > 4:
    eeg_config = sys.argv[4]
else:
    eeg_config = ""
     

if parameters > 4 and "verbose" in eeg_config:
    verbose = True
else:
    verbose = False

if parameters > 4 and "path" in eeg_config:
    mirror.text("[Python Search Path] " + str(sys.path))


#  Setup [ pyUSB (Default) / pywinusb ]
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
if parameters > 4 and "pywinusb" in eeg_config:
    if verbose == True:
        mirror.text("> Importing (pywinusb) \\cyPyWinUSB")
    
    eeg_driver = "pywinusb"
    sys.path.insert(0, localPath + '\\cyPyWinUSB')
    import cyPyWinUSB as hid
else:
    if verbose == True:
        mirror.text("> Importing (pyusb) \\cyPyUSB")
    eeg_driver = "pyusb"
    sys.path.insert(0, localPath + '\\cyUSB')
    sys.path.insert(0, localPath + '\\cyUSB\\libusb')
    import cyPyUSB
    import cyPyUSB.core
    import cyPyUSB.util
    import cyPyUSB.backend.libusb1

if parameters > 4 and "bluetooth" in eeg_config:
    
    BT_manualkey = "AUTO-DETECT"    
    
    if "bluetooth=" in eeg_config:
        split_bt = str(eeg_config).split("bluetooth=")
        
        if len(split_bt) > 1:
            if "+" in split_bt[1]:
                BT_manualkey = str(split_bt[1]).split("+")[0]
            else:
                BT_manualkey = split_bt[1]

            if len(BT_manualkey) > 8 or len(BT_manualkey) < 8:
                mirror.text("> Incorrect Key Length. Bluetooth key is 8 hex digits long. ")
                mirror.text("> (Locate in the EPOC+(xxxxxxxx) title, in Windows Bluetooth settings.)")
                mirror.text("\r\n> Defaulting to auto-detect bluetooth. ")
    
    mirror.text("\r\n> Trying Bluetooth Key >>> " + str(BT_manualkey))
    sys.path.insert(0, localPath + '.\\cyDrivers') 

    try:
        eegDLL = cdll.LoadLibrary(localPath + "\\cyDrivers\EEGBtleLib" + str(arch) + ".dll")
        
    except Exception as e:
        mirror.text("> Bluetooth Library not loaded. ")
        mirror.text(" Error " + str(e))
        os._exit(0)
    
    eeg_driver = "bluetooth"

#  Import modified pycryptodomex AES ciphers.
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
from cyCrypto.Cipher import AES
from cyCrypto.Random import get_random_bytes
from cyCrypto.Util.Padding import pad

tasks = queue.Queue()
encrypted_data = bytearray()

#  Bluetooth LE. Data Structure Function.
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
class BTH_LE_GATT_CHARACTERISTIC_VALUE(Structure):
        global _CB_FUNC_
        _fields_ = [
            ("DataSize", c_ulong),
            ("Data", c_ubyte * 20)] 

_CB_FUNC_ = CFUNCTYPE(None, BTH_LE_GATT_CHARACTERISTIC_VALUE)            


#  ControllerIO(). I/O threaded bridge to browser (for CyWebSocket.py and eeg.py)
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
class ControllerIO():
    
    #  Initialize at thread creation.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def __init__(self):
        global BTLE_device_name
        BTLE_device_name = ""
        self.integer = False
        self.noheader = False
        self.ovdelay = 100
        self.ovsamples = 4
        self.openvibe = False
        self.generic = False
        self.format = 0;
        self.newMask = None
        self.status = False
        self.setMask = []
        self.infoData = {}
        self.setMask = [None]*14
        self.recordInc = 1
        self.recordFile = "EEG_recording_"
        self.delimiter = ", "
        self.samplingRate = 128
        self.channels = 40
        self.baseline_data = None
        self.baseline = False
        self.datamode = 1
        self.cyFile = None
        self.device = None
        self.packet_count = 0
        self.setInfo("recording","False")
        
    #  Data Input.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def onData(self, uid, text):
        
        ioCommand = text.split(":::")
        if ioCommand[0] == "CyKITv2":
            if ioCommand[1] == "setModel":
                self.newModel = int(ioCommand[2])
                mirror.text("model=" + ioCommand[2])
            
            if ioCommand[1] == "getDataMode":
                mirror.text("Sending >>> datamode:::" + str(self.getInfo("datamode")))
                self.server.sendData(1, "CyKITv2:::Info:::datamode:::" + str(self.getInfo("datamode")))
            
            if ioCommand[1] == "setDataMode":
                self.datamode = int(ioCommand[2])
                self.setInfo("datamode",str(self.datamode))
                if eval(self.getInfo("verbose")) == True:
                    mirror.text(">>> Client Setting >>> DataMode = " + str(self.datamode))
                return
                
            if ioCommand[1] == "changeFormat":
                self.format = int(ioCommand[2])
                if self.format == 1:
                    mirror.text("Format Change (Format-1): Javascript handling float conversion.\r\n")
                else:
                    mirror.text("Format Change (Format-0): Python handling float conversion.\r\n")
                self.setInfo("format", str(self.format))

            if ioCommand[1] == "Disconnect":
                self.server.onClose("browser")
                self.setInfo("status","False")
                self.onClose("browser")
                return
            
            if ioCommand[1] == "InfoRequest":
                self.server.sendData("CyKITv2:::Info:::device:::" + str(self.getInfo(["device"])))
                self.server.sendData("CyKITv2:::Info:::serial:::" + str(self.getInfo(["serial"])))

            if ioCommand[1] == "UpdateSettings":
                self.setInfo("updateEPOC", ioCommand[2])
                if "DeviceObject" in self.infoData and self.getInfo("intf") != None:
                    settings_menu(self.infoData["DeviceObject"], self, self.getInfo("intf"))
                else:
                    mirror.text("> Device Object not found.")
            
            if ioCommand[1] == "getBaseline":
                if self.baseline_data != None:
                    self.server.sendData("CyKITv2:::Baseline:::" + str(self.baseline_data))
                        
            if ioCommand[1] == "setBaselineMode":
                if ioCommand[2] == "1":
                    self.baseline = True
                else:
                    self.baseline = False
                
                self.setInfo("baselinemode",str(self.baseline))
                return
                        
            if ioCommand[1] == "RecordStart":
                if eval(self.getInfo("recording")) == True:
                    self.stopRecord()
                    mirror.text("[Record Stopped] -- Press 'Record' to Record a new file.")
                    return
                
                self.recordFile = str(ioCommand[2])
                
                cyPath = os.path.realpath("")
                if os.path.exists(cyPath + "/EEG-Logs") == False:
                    try:
                        os.mkdir(cyPath + "/EEG-Logs")
                    except Exception as msg:
                        mirror.text("*** Failed to Create Directory: '" + cyPath + "/EEG-Logs/' \r\n Please Check Permissions. ")
                        mirror.text(str(msg))
                        return
                        
                pathFinder = cyPath + "/EEG-Logs/" + self.recordFile + '.csv'
                if os.path.exists(pathFinder):
                    if "_" not in self.recordFile:
                        self.recordFile += "_0"
                    
                    if len(self.recordFile.split("_")[1]) == 0:
                        self.recordFile += "0"
                        
                    if self.recordFile.split("_")[1].isdigit() == False:
                        self.recordFile = self.recordFile.split("_")[0] + "_0"
                    
                    mirror.text(self.recordFile)
                    fileIndex = int(self.recordFile.split("_")[1])
                    self.recordInc = fileIndex
                try:
                    while os.path.exists(pathFinder):
                        self.recordInc += 1
                        self.recordFile = self.recordFile.split("_")[0] + "_" + str(self.recordInc)
                        pathFinder = cyPath + "/EEG-Logs/" + self.recordFile + ".csv"
                        if eval(self.getInfo("verbose")) == True:
                            mirror.text("[Record: File exists. Changing to: " + self.recordFile + ".csv ]")
                except Exception as msg:
                    mirror.text("File Selection Error: " + str(msg))
                    return
                
                mirror.text("[Start] Recording to File: " + self.recordFile + " \r\n")
                try:
                    self.cyFile = open(cyPath + "\\EEG-Logs\\" + self.recordFile + ".csv", "w+" ,newline='')
                    #mirror.text(str(dir(self.f)))
                    csvHeader = ""
                    csvHeader += "title: " + self.recordFile + ", "
                    csvHeader += "recorded: " + str(time.strftime("%d.%m.%y %H.%M.%S, "))
                    csvHeader += "timestamp started:2017-11-21T16:17:43.558438-08:00            , "
                    csvHeader += "sampling:" + str(self.samplingRate) + ", "
                    csvHeader += "subject:, "
                    csvHeader += "labels:COUNTER INTERPOLATED "
                    if int(self.getInfo("keymodel")) == 3 or int(self.getInfo("keymodel")) == 4:
                        # Insight
                        csvHeader += "AF3 T7 Pz T8 AF4 RAW_CQ GYROX GYROY MARKER SYNC TIME_STAMP_s TIME_STAMP_ms CQ_AF3 CQ_T7 CQ_Pz CQ_T8 CQ_AF4, "
                    else:
                        # Epoc/Epoc+
                        #csvHeader += "AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4 "
                        csvHeader += "F3 FC5 AF3 F7 T7 P7 O1 O2 P8 T8 F8 AF4 FC6 F4 "
                        csvHeader += "RAW_CQ GYROX GYROY MARKER MARKER_HARDWARE SYNC TIME_STAMP_s TIME_STAMP_ms "
                        csvHeader += "CQ_AF3 CQ_F7 CQ_F3 CQ_FC5 CQ_T7 CQ_P7 CQ_O1 CQ_O2 CQ_P8 CQ_T8 CQ_FC6 CQ_F4 CQ_F8 CQ_AF4 CQ_CMS CQ_DRL, "
                    csvHeader += ", "
                    csvHeader += "chan:" + str(self.getInfo("channels")) + ", "
                    csvHeader += "samples:, "
                    csvHeader += "units:emotiv"

                    self.cyFile.write(csvHeader + "\r\n")
                    self.cyFile.flush()
                    os.fsync(self.cyFile.fileno())
                    self.setInfo("recording","True")
                    self.packet_count = 0

                except Exception as e:
                    exc_type, ex, tb = sys.exc_info()
                    imported_tb_info = traceback.extract_tb(tb)[-1]
                    line_number = imported_tb_info[1]
                    print_format = "{}: Exception in line: {}, message: {}"
                    mirror.text(" ¯¯¯¯ eegThread.run() Error Communicating With USB.")
                    mirror.text(" =E.3: " + print_format.format(exc_type.__name__, line_number, ex))    
                    return
                
            if ioCommand[1] == "RecordStop":
                if eval(self.getInfo("recording")) == False:
                    return
                mirror.text("[Stop] Recording \r\n")
                mirror.text(("═" * 50))
                self.setInfo("total_packets", str(self.packet_count))
                mirror.text(" Recorded File: " + self.recordFile + "\r\n Packet Count: " + str(self.packet_count))
                mirror.text(("═" * 50))
                self.stopRecord()
                
            if ioCommand[1] == "setMask":
                try:
                    maskSelect = int(ioCommand[2])
                    self.newMask = maskSelect
                    self.setMask[maskSelect] = map(int, str(ioCommand[3]).split(","))
                except Exception as msg:
                    mirror.text("Recording Write Error: " + str(msg))

        return
    
    def onConnect(self, uid):
        self.setInfo("status","True")
        self.newMask = None
        if self.openvibe == True:
            return
        if self.noheader == True:
            return
        self.server.sendData("CyKITv2:::Connected")
        return
        
    def setBaselineMode(self, status):
        self.baseline = status
        self.setInfo("baselinemode",str(status))
        return
    
    def getBaselineMode(self):
        
       
        return self.baseline
    
    def getBaseline(self):
        
       
        if self.baseline_data == None:
            return
        return self.baseline_data
    
    def setBaseline(self, set_data):
        
       
        self.baseline_data = set_data
        return
        
    def onGeneric(self, uid):
        self.setInfo("status","True")
        self.setInfo("generic","True")
        if eval(self.getInfo("openvibe")) == True:
            return
        if eval(self.getInfo("noheader")) == True:
            return
        self.server.sendData("CyKITv2:::Connected")
        return
    
    def sendOVint(self, data):
        self.server.sendOVint(data)
        return
    
    def sendOVfloat(self, data):
        self.server.sendOVfloat(data)
        return
    
    def sendData(self, uid, data):
        if self.openvibe == True:
            return
        try:
            self.server.sendData(data)
        except:
            return
        return      
        
    def status(self):
        return self.getInfo("status")
    
    def onClose(self, location):
        if eval(self.getInfo("verbose")) == True:
            mirror.text("*** Connection Closing. (Location: " + location + ")")
        self.status = False
        self.setInfo("status","False")
        return
    
    def modelChange(self):
    
        if 'newModel' not in globals():
            return 0
        aModel = self.newModel
        self.newModel = 0
        return self.aModel
         
    def startRecord(self, recordPacket):
        if eval(self.getInfo("recording")) == False:
            return
        try:
            self.packet_count += 1
            self.cyFile.write(recordPacket + "\r\n")
            self.cyFile.flush()
            os.fsync(self.cyFile.fileno())
        except:
            pass

    def stopRecord(self):
        if eval(self.getInfo("recording")) == False or self.cyFile == None:
            return
        
        self.setInfo("recording","False")
        try:
            
            #Update File.
            self.cyFile.flush()
            os.fsync(self.cyFile.fileno())
            
            #Remove \r\n at EOF.
            self.cyFile.seek(0, os.SEEK_END)
            f_size = self.cyFile.tell()
            self.cyFile.truncate((f_size -2))
            
            #Add Sample Count to CSV header.
            self.cyFile.seek(0,0)
            sampleData = self.cyFile.read()
            if "samples:" in sampleData:
                writeSamples = sampleData.replace("samples:","samples:" + str((int(self.packet_count) -1)))
                self.cyFile.seek(0,0)
                self.cyFile.write(writeSamples)
             
            #Update and Close.
            self.cyFile.flush()
            os.fsync(self.cyFile.fileno())
            self.cyFile.close()
            self.cyFile = None
            
        except Exception as msg:
            mirror.text("Recording Write Error: " + str(msg))
            pass
        
    def formatStatus(self):
        return self.format
        
    def isRecording(self):
        return eval(self.getInfo("recording"))

    def maskChange(self):
        return self.newMask
    
    def getMask(self, select):
        self.newMask = None
        return self.setMask[int(select)]
    
    def setReport(self, report):
        self.report = report
        self.epoc_plus_usb = True
    
    #  Set Information. (Name, Info)
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def setInfo(self, name, info):
        if "str" in str(type(info)):
            self.infoData[str(name)] = str(info)
        else:
            self.infoData[name] = info # Preserve Object
        return
        
    #  Retrieve Information by Name. 
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def getInfo(self, name):
        if str(name) not in self.infoData:
            return "0"
        else:
            return self.infoData[str(name)]
        
    # Send Info to Server.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def sendInfo(self, name):
        if name not in self.infoData:
            self.server.sendData("CyKITv2:::Info:::" + str(name) + ":::None")
            return
        self.server.sendData("CyKITv2:::Info:::" + str(name) + ":::" + str(self.infoData[str(name)]))
        return
    
    # Set Server Object.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def setServer(self, server):
        self.server = server
        return

def resolve_mode(dataSTR):
    changed_mode = -1
    if dataSTR == str([0, 0, 128, 14, 128, 12, 0 ,0]):
        changed_mode = 0
        
    if dataSTR == str([1, 0, 128, 16, 0, 16, 0, 0]):
        changed_mode = 1
        
    if dataSTR == str([1, 0, 128, 16, 32, 16, 0, 0]):
        changed_mode = 2
        
    if dataSTR == str([1, 0, 128, 16, 64, 16, 0, 0]):
        changed_mode = 3
        
    if dataSTR == str([1, 0, 128, 16, 128, 16, 0, 0]):
        changed_mode = 4
    
    if dataSTR == str([1, 1, 0, 16, 0, 16, 0, 0]):
        changed_mode = 5
    
    if dataSTR == str([1, 1, 0, 16, 32, 16, 0, 0]):
        changed_mode = 6
    
    if dataSTR == str([1, 1, 0, 16, 64, 16, 0, 0]):
        changed_mode = 7
    
    if dataSTR == str([1, 1, 0, 16, 128, 16, 0, 0]):
        changed_mode = 8
    
    return changed_mode
    
def settings_menu(device, sIO, intf):
    
    data = None
    current_txt = "unknown"
    current_mode = -1
    current = ["","","","","","","","",""]
    
    if eeg_driver == "pyusb":
        device_firmware   = sIO.getInfo("deviceFirmware")
        software_firmware = sIO.getInfo("softFirmware")
        
        if device_firmware != "0x565" or software_firmware != "0x625":
            mirror.text("Hardware Information indicates your firmware might not be supported for mode changes via CyKIT")
            mirror.text("   Please Report your firmware and software to the software developer:")
            mirror.text("   Device   Firmware: " + device_firmware)
            mirror.text("   Software Firmware: " + software_firmware)
            mirror.text("\r\n Until it is concluded to be safe to update via CyKIT, ")
            mirror.text("  it is recommended you use an Emotiv program to make mode changes.")
            
    if eeg_driver == "pywinusb":
        successReport = device.find_input_reports()
        
        for inputReport in successReport:
            mirror.text(str(inputReport.get_hid_object()))
            data = inputReport.get()
        
    if data != None:
        current_mode = resolve_mode(str(data[12:20]))
        
        if current_mode != -1:
            current_txt = str(current_mode)
            current[current_mode] = "* (Active)"
        
        current[current_mode] 
                
    if sIO.getInfo("updateEPOC") != "None":
        mode_select = sIO.getInfo("updateEPOC")
        sIO.setInfo("updateEPOC", "None")
    else:
        mirror.text("\r\n")
        mirror.text("═" *100)
        mirror.text("  *** Important Advisories *** (Please Read)              ")
        mirror.text("═" *100)
        mirror.text("      The EPOC+ is connected directly to your computer via USB.                                                     ")
        mirror.text("      During this time, the device can not send data via Bluetooth or USB. \r\n\r\n                                 ")
        mirror.text("      To Change the EPOC+ mode, the device must be [Powered On] (ie. White light on)  while connected to USB.       ")
        mirror.text("      If the device is not turned on when a selection is made, no settings will be changed.\r\n\r\n                 ")
        mirror.text("      Changing to 256hz and or enabling MEMS (ie. gyro) data, will reduce the battery life.                         ")
        mirror.text("      EPOC+ (Typical) Battery Life = 12 Hours. \r\n\r\n                                                             ")
        mirror.text("      EPOC+ (14-bit mode) - key model# = 4                                                                               ")
        mirror.text("      EPOC+ (16-bit mode) - key model# = 6 \r\n                                                                      \r\n")
        mirror.text("═" *100)
        
        mirror.text("  EPOC+ Mode Selection Menu. [Current Mode: " + current_txt + "]")
        mirror.text("═" *100)
        mirror.text(" 0) EPOC (14-bit mode)                       " + str(current[0]))
        mirror.text(" 1) EPOC+ 128hz 16bit - MEMS off             " + str(current[1]))
        mirror.text(" 2) EPOC+ 128hz 16bit - MEMS 32hz  16bit     " + str(current[2]))
        mirror.text(" 3) EPOC+ 128hz 16bit - MEMS 64hz  16bit     " + str(current[3]))
        mirror.text(" 4) EPOC+ 128hz 16bit - MEMS 128hz 16bit     " + str(current[4]))
        mirror.text(" 5) EPOC+ 256hz 16bit - MEMS off             " + str(current[5]))
        mirror.text(" 6) EPOC+ 256hz 16bit - MEMS 32hz  16bit     " + str(current[6]))
        mirror.text(" 7) EPOC+ 256hz 16bit - MEMS 64hz  16bit     " + str(current[7]))
        mirror.text(" 8) EPOC+ 256hz 16bit - MEMS 128hz 16bit     " + str(current[8]) + "\r\n")
        mode_select = input(" Enter Mode: [0,1,2,3,4,5,6,7,8] or [Q] to Exit \> ")
    
    if mode_select.upper() == "Q":
        os._exit(0)
        
        
    if mode_select.isdigit() == True:
        mode_select = int(mode_select)
        if mode_select > -1 and mode_select < 9:
                
            EPOC_ChangeMode = mode_select
            
            ep_mode = [0x0] * 32
            if eeg_driver == "pywinusb":
                ep_mode[1:4] = [0x55,0xAA,0x20,0x12] 
                ep_select = [0x00,0x82,0x86,0x8A,0x8E,0xE2,0xE6,0xEA,0xEE]
                ep_mode[5] = ep_select[EPOC_ChangeMode]
            if eeg_driver == "pyusb":
                ep_mode[0:3] = [0x55,0xAA,0x20,0x12] 
                ep_select = [0x00,0x82,0x86,0x8A,0x8E,0xE2,0xE6,0xEA,0xEE]
                ep_mode[4] = ep_select[EPOC_ChangeMode]

            #0 EPOC                                  0x00 (d.000)  55 AA 20 12 00     IN
            #1 EPOC+ 128hz 16bit - MEMS off          0x82 (d.130)  55 AA 20 12 82 00  IN 
            #2 EPOC+ 128hz 16bit - MEMS 32hz 16bit   0x86 (d.134)  55 AA 20 12 86     IN    55 AA 88 12 00
            #3 EPOC+ 128hz 16bit - MEMS 64hz 16bit   0x8A (d.138) 
            #4 EPOC+ 128hz 16bit - MEMS 128hz 16bit  0x8E (d.142)
            #5 EPOC+ 256hz 16bit - MEMS off          0xE2 (d.226)
            #6 EPOC+ 256hz 16bit - MEMS 32hz 16bit   0xE6 (d.230)
            #7 EPOC+ 256hz 16bit - MEMS 64hz 16bit   0xEA (d.234)
            #8 EPOC+ 256hz 16bit - MEMS 128hz 16bit  0xEE (d.238)
            
            mirror.text("\r\n>>> Sending Mode Update to EPOC+ >>> \r\n\r\n")
            try:
                if eeg_driver == "pywinusb":
                    
                    report = device.find_output_reports()
                    report[0].set_raw_data(ep_mode)
                    report[0].send()
                    mirror.text("*** Updated EPOC+ Settings ***")
                    
                    changed_mode = -1
                    wait_for_mode = 0
                    
                    while changed_mode != EPOC_ChangeMode:
                        wait_for_mode += 1
                        if wait_for_mode > 10000:
                            mirror.text("\r\n\r\n> Mode change incomplete. Please try again. ")
                            mirror.text("\r\n> Confirm the device is turned on during update. *** ")
                            os._exit(0)
                            
                        for inputReport in successReport:
                            data = inputReport.get()
                            dataSTR = str(data[12:20])
                            #using STR comparison instead of built-in SET due to py error.
                            changed_mode = resolve_mode(dataSTR)
                            
                    mirror.text("\r\n>>> (Confirmation) >>> EPOC+ Mode Changed to: " + str(changed_mode) + " \r\n\r\n")
                            
                if eeg_driver == "pyusb":
                    if intf == None:
                        mirror.text("> Invalid Descriptor ")
                        os._exit(0)
                    report = cyPyUSB.util.find_descriptor(intf, custom_match = \
                                                          lambda e: cyPyUSB.util.endpoint_direction(e.bEndpointAddress) == cyPyUSB.util.ENDPOINT_OUT)
                    report.write(ep_mode)
                    
                    
            except Exception as e:
                exc_type, ex, tb = sys.exc_info()
                imported_tb_info = traceback.extract_tb(tb)[-1]
                line_number = imported_tb_info[1]
                print_format = "{}: Exception in line: {}, message: {}"
                mirror.text(" ¯¯¯¯ eegThread.run() Error Communicating With USB.")
                mirror.text(" =E.3: " + print_format.format(exc_type.__name__, line_number, ex))    
                os._exit(0)
        
                
            
                    
def DataCallback(EventOutParameter):
        global encrypted_data

        if BTLE_device_name == "":
            return

        try:
            data_bin = EventOutParameter.Data
        except Exception as e: 
            mirror.text(" Bluetooth Error: " + str(e))
            return

        if data_bin == "":
            return

        if BTLE_device_name == "Insight":
            tasks.put(bytearray(data_bin))
            return

        if len(data_bin) < 18:
            if 'encrypted_data' in locals():
                del encrypted_data
            return

        

        if data_bin[1] == 1:
            if 'encrypted_data' in locals():
                del encrypted_data
            encrypted_data = bytearray(data_bin[2:18])
        
        if data_bin[1] == 2:
            if 'encrypted_data' in globals():
                if len(encrypted_data)  < 16:
                    return
                encrypted_data = encrypted_data + bytearray(data_bin[2:18])
                tasks.put(encrypted_data)

class EEG(object):

    def __init__(self, model, io, config):
        global running
        global cyIO
        
        config = config.lower()
        self.config = config
        self.time_delay = .001
        self.KeyModel = model
        self.running = True
        self.counter = "0"
        self.serial_number = ""
        self.lock = threading.Lock()
        self.cyIO = io
        self.cyIO.setInfo("updateEPOC","None") # Must be set before Setup()
        self.device = None                             # Must be set before Setup()
        self.myKey = self.Setup(model, config)
        self.recordInc = 1
        self.thread_1 = threading.Thread(name='eegThread', target=self.run, kwargs={'key': self.myKey, 'cyIO': self.cyIO}, daemon = False)
        self.stop_thread = False
        self.samplingRate = 128
        self.epoc_plus_usb = False
        self.report = None
        self.channels = 40
        self.blankcsv = False
        self.generic = False
        self.openvibe = False
        self.integer = False
        self.noheader = False
        self.blankdata = False
        self.nocounter = False
        self.nobattery = False
        self.baseline = False
        self.outputdata = False
        self.outputraw = False
        self.verbose = False
        self.noweb = False
        self.filter = False
        self.datamode = 1
        self.getSeconds = 0
        self.baseSeconds = 0
        
        self.mask = {}
        self.mask[0] = [10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7]
        self.mask[1] = [28, 29, 30, 31, 16, 17, 18, 19, 20, 21, 22, 23, 8, 9]
        self.mask[2] = [46, 47, 32, 33, 34, 35, 36, 37, 38, 39, 24, 25, 26, 27]
        self.mask[3] = [48, 49, 50, 51, 52, 53, 54, 55, 40, 41, 42, 43, 44, 45]
        self.mask[4] = [66, 67, 68, 69, 70, 71, 56, 57, 58, 59, 60, 61, 62, 63]
        self.mask[5] = [84, 85, 86, 87, 72, 73, 74, 75, 76, 77, 78, 79, 64, 65]
        self.mask[6] = [102, 103, 88, 89, 90, 91, 92, 93, 94, 95, 80, 81, 82, 83]
        self.mask[7] = [140, 141, 142, 143, 128, 129, 130, 131, 132, 133, 134, 135, 120, 121]
        self.mask[8] = [158, 159, 144, 145, 146, 147, 148, 149, 150, 151, 136, 137, 138, 139]
        self.mask[9] = [160, 161, 162, 163, 164, 165, 166, 167, 152, 153, 154, 155, 156, 157]
        self.mask[10] = [178, 179, 180, 181, 182, 183, 168, 169, 170, 171, 172, 173, 174, 175]
        self.mask[11] = [196, 197, 198, 199, 184, 185, 186, 187, 188, 189, 190, 191, 176, 177]
        self.mask[12] = [214, 215, 200, 201, 202, 203, 204, 205, 206, 207, 192, 193, 194, 195]
        self.mask[13] = [216, 217, 218, 219, 220, 221, 222, 223, 208, 209, 210, 211, 212, 213]
        
        self.insight_1 = [0,8,14,22,28,36,42,50,56,64,70,78,84,92,98,106,112,120,126,134,140,148,154,162,168,176,182,190,196,204,210,218,224,232,238]
        self.insight_2 = [0,8,14,22,28,36,42,50,56,64]
        
        self.blank_data = {}
        # BlankData for Epoc??
        self.blank_data[2] = [0, 11, 45, 226, 13, 209, 11, 156, 77, 16, 118, 83, 208, 255, 75, 10, 40, 241, 206, 231, 146, 226, 59, 124, 165, 69, 24, 248, 163, 55, 25, 133, 167]        
        self.blank_data[6] = [0, 16, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 0, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128, 0, 128]
        
        self.configFlags = ["blankdata","blankcsv","nocounter","nobattery","baseline","noheader",
                       "integer","outputdata","generic","openvibe","baseline","outputraw",
                       "filter","allmode","eegmode","gyromode","verbose","noweb"]

        if "allmode" in config:       self.datamode = 0
        if "eegmode" in config:       self.datamode = 1
        if "gyromode" in config:      self.datamode = 2       
        
        if "nocounter" in config:     
            self.nocounter = True
            if self.datamode == 0:
                self.datamode = 1
        else:   self.nocounter = False
        
        if "ovdelay" in config:      
            myDelay = str(config).split("ovdelay:")
            self.ovdelay = myDelay[1][:3]
        else:                        
            self.ovdelay = 100
            
        if "ovsamples" in config:      
            mySamples = str(config).split("ovsamples:")
            self.ovsamples = int(mySamples[1][:3])
            if self.ovsamples > 512:
                self.ovsamples = 512
        else:                        
            self.ovsamples = 4
        
        if "delimiter" in config:     
            nDelimiter = str(config).split("delimiter=")[1]
            if len(nDelimiter) > 0:
                if "+" in nDelimiter:
                    nDelimiter = str(nDelimiter).split("+")[0]
                if nDelimiter.isdigit() and abs(int(nDelimiter)) < 1114112:
                    self.delimiter = chr(abs(int(nDelimiter)))
                else:
                    self.delimiter = ","
        else:
            self.delimiter = ","
        
        if "format" in config:     
            myFormat = str(config).split("format-")
            self.format = int(myFormat[1][:1])
        else:
            self.format = 0
            
        if "channel=" in config:     
            channel_select = str(config).split("channel=")[1]
            
            if "+" in channel_select:
                self.channel = str(channel_select).split("+")[0]
                
            else:
                self.channel = channel_select[0]
            if self.channel == "":
                self.channel == None
        else:
            self.channel = None
        
        
        if eval(self.cyIO.getInfo("verbose")) == True:
            mirror.text("    Format = " + str(self.format))
            try:
                mirror.text(" Delimiter = " + str(self.delimiter))
            except:
                self.delimiter = ","
                mirror.text(" Delimiter = " + str(self.delimiter))
                
                pass
            
            
        
        #  Set Config Flags and Insert Into Dictionary.
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        if eval(self.cyIO.getInfo("verbose")) == True:
            mirror.text("═" *90 + "\r\n")
            mirror.text(" Config Options = { \r\n")
        for index in self.configFlags:
            if str(index) in config:
                if eval(self.cyIO.getInfo("verbose")) == True:
                    mirror.text("   " + index + (chr(9)*2) + " " + str(True) + "  *")
                locals()['self.' + index] = True
            else:
                if eval(self.cyIO.getInfo("verbose")) == True:
                    mirror.text("   " + index + (chr(9)* 2) + str(False))
                locals()['self.' + index] = False
            self.cyIO.setInfo(index,str(locals()['self.' + index]))
        
        self.cyIO.setInfo("ovsamples", self.ovsamples)
        self.cyIO.setInfo("delimiter", self.delimiter)
        self.cyIO.setInfo("datamode", self.datamode)
        self.cyIO.setInfo("format", self.format)
        self.cyIO.setInfo("config", config)
        
        if eval(self.cyIO.getInfo("verbose")) == True:
            mirror.text("\r\n }")
        mirror.text("═" *50 + "\r\n")
        
        
    def start(self):
        
        self.running = True
        self.status = True
        for t in threading.enumerate():
            if 'eegThread' == t.getName():
                return self.cyIO
                self.thread_1.start()
                
        
        self.thread_1.start()
        return self.cyIO

    
    def Setup(self, model, config):
        global BTLE_device_name
       
        #  Additional Product Names. (Not used for Data)
        # 'EPOC BCI', 'Brain Waves', 'Brain Computer Interface USB Receiver/Dongle', 'Receiver Dongle L01'
        deviceList  = ['EPOC+','EEG Signals', '00000000000', 'Emotiv RAW DATA', "FLEX"]

        devicesUsed = 0        
        threadMax = 0
        detail_info = None
        device_firmware = ""
        software_firmware = ""
        intf = 0
        
        for t in threading.enumerate():
            if t.getName()[:6] == "Thread": 
                threadMax += 1
        
        #  Bluetooth LE
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        if eeg_driver == "bluetooth":
            
            DEVICE_UUID = "{81072f40-9f3d-11e3-a9dc-0002a5d5c51b}"
            DATA_UUID   = "{81072f41-9f3d-11e3-a9dc-0002a5d5c51b}"
            MEMS_UUID   = "{81072f42-9f3d-11e3-a9dc-0002a5d5c51b}"

            eegDLL.get_bluetooth_id.restype     =  c_wchar_p  # Result   type: C-style character pointer. 

            eegDLL.btle_init.argtypes           = [c_wchar_p] # Argument type: C-style character pointer.    
            eegDLL.btle_init.restype            =  c_void_p   # Argument type: C-style pointer.

            eegDLL.set_callback_func.argtypes   = [c_void_p]  # Pointer for callback function.
            eegDLL.set_callback_func.restype    =  c_void_p   # Pointer for device handle.

            eegDLL.run_data_collection.argtypes = [ c_void_p, POINTER(c_wchar_p * 2) ] # Pointer, Pointer to UUID array.
            eegDLL.run_data_collection.restype  =   c_void_p                           # Pointer.

            BT_manualkey = globals()['BT_manualkey']
            
            uuid_list = [str(DATA_UUID), str(MEMS_UUID)]
            uuid_clist = (c_wchar_p * len(uuid_list))()
            uuid_clist[:] = uuid_list

            try:
                global _CB_FUNC_
                global cb
                
                self.device = eegDLL.btle_init(DEVICE_UUID) # Open.
                cb = _CB_FUNC_(DataCallback)                    # Set Handler.
                eegDLL.set_callback_func(cb)             
                #mirror.text("> Searching for Bluetooth Device . . .")
                useDevice = ""
                while useDevice != "Y":
                    getBTname = eegDLL.get_bluetooth_id()
                    
                    time.sleep(1)
                    BTid = str(c_wchar_p(getBTname).value)
                    
                    if "EPOC" in BTid or "Insight" in BTid: 
                        mirror.text("\r\n> Found Bluetooth Device: [" + BTid  + "] \r\n")
                        if "confirm" in config:
                            useDevice = input(" Use this device? [Y]es? ").upper()
                        else:
                            useDevice = "Y"
                        
                        if useDevice == "Y":
                            BTid = BTid.replace("(","")
                            BTid = BTid.replace(")","")
                            BT_key = BTid.split(" ")
                            BTLE_device_name = BT_key[0]
                            BT_key = BT_key[1]
                            if BT_manualkey != "AUTO-DETECT" and BT_manualkey != BT_key:
                                useDevice = ""
                                continue
                            
                            self.serial_number = bytes(("\x00" * 12),'utf-8') + bytearray.fromhex(str(BT_key[6:8] + BT_key[4:6] + BT_key[2:4] + BT_key[0:2]))
                    
                
                BT_Run = eegDLL.run_data_collection(self.device, uuid_clist)

                devicesUsed +=1

                self.product_name = "EEG Signals"
        
            except Exception as e:
                mirror.text("> Error Initializing Bluetooth. ")
                mirror.text(" Bluetooth Setup() Error:" + str(e))
                return
                os._exit(0)
            
        
        #  PyWinUSB.
        # ¯¯¯¯¯¯¯¯¯¯¯¯
        if eeg_driver == "pywinusb" and self.device == None:
            try:
                for all_devices in hid.find_all_hid_devices():
                    if "info" in config:
                        
                        mirror.text("Product name " + self.product_name)
                        mirror.text("device path " + all_devices.device_path)
                        mirror.text("instance id " + all_devices.instance_id)
                        mirror.text("═" * 50 + "\r\n")
                    useDevice = ""
                    for i, findDevice in enumerate(deviceList):
                        
                        if all_devices.product_name == deviceList[i]:
                            mirror.text("\r\n> Found EEG Device: [" +  findDevice + "] \r\n")
                            if "confirm" in config:
                                useDevice = input("Use this device? [Y]es? ")
                            else:
                                useDevice = "Y"
                            if useDevice.upper() == "Y":
                                devicesUsed += 1
                                self.device = all_devices
                                if threadMax < 2:
                                    self.device.open()
                                self.product_name = all_devices.product_name
                                self.serial_number = all_devices.serial_number
                                if threadMax < 2:
                                    all_devices.set_raw_data_handler(self.dataHandler)
                                    detail_info = None
                                    device_firmware = ""
                                    while detail_info == None:
                                        detail_report = self.device.find_input_reports()
                                        detail_info   = detail_report[0].get()
                                        mirror.text(str(detail_info))
                                        device_firmware = "0x" + str(hex(detail_info[3]))[2:] +  str(hex(detail_info[4])[2:])
                                    if eval(self.cyIO.getInfo("verbose")) == True:
                                        mirror.text(" USB Dongle Firmware = " + device_firmware)
                                        
                                mirror.text("> Using Device: " + all_devices.product_name + "\r\n")
                                mirror.text("  Serial Number >>> " + all_devices.serial_number)
                                if all_devices.product_name == "EPOC+":
                                    deviceList[1] = "empty" # Direct USB Connection detected. Replace EEG Signals to avoid connecting.
                                    #self.cyIO.setReport("Device", all_devices.find_output_reports())
                                    
            except Exception as msg:
                mirror.text(" Device Error: " + str(msg))
             
        #  PyUSB.
        # ¯¯¯¯¯¯¯¯¯
        if eeg_driver == "pyusb" and self.device == None:
            try:
                # Alternative 'backend' devices for pyUSB, could be added here.
                backend = cyPyUSB.backend.libusb1.get_backend(find_library=lambda x: "./cyDrivers/libusb-1.0x" + str(arch) + ".dll")
                
                if str(backend) == "None":
                   mirror.text("> Driver could not be found or unsuccessfully loaded.")
                   os._exit(0)
                self.product_name = None
                all_devices = cyPyUSB.core.find(find_all=1, backend=backend)
                for select_device in all_devices:
                    if eval(self.cyIO.getInfo("verbose")) == True:
                        mirror.text("═" * 50)
                    try:
                        company = str(cyPyUSB.util.get_string(select_device, select_device.iManufacturer))
                        product = str(cyPyUSB.util.get_string(select_device, select_device.iProduct))
                        
                        vid     = str(hex(select_device.idVendor))
                        pid     = str(hex(select_device.idProduct))
                    except:
                        mirror.text("> USB Device (No Additional Information)")
                        continue
                    if eval(self.cyIO.getInfo("verbose")) == True:
                        mirror.text(" Company: " + company)
                        mirror.text("  Device: " + product)
                        mirror.text("  Vendor: " + vid)
                        mirror.text(" Product: " + pid)

                    useDevice = ""
                    for i, findDevice in enumerate(deviceList):
                        
                        if product == deviceList[i]:
                            
                            mirror.text("\r\n> Found EEG Device [" +  findDevice + "] \r\n")
                            if "confirm" in config:
                                useDevice = input(" Use this device? [Y]es? ")
                            else:
                                useDevice = "Y"
                            if useDevice.upper() == "Y":
                                devicesUsed += 1
                                self.device = select_device

                                if threadMax < 2:
                                    
                                    self.device.set_configuration()
                                    cfg = self.device.get_active_configuration()
                                    
                                    if product == 'EPOC+':
                                        deviceList[1] = 'empty'
                                        intf = cfg[(0,0)]
                                        self.cyIO.setInfo("intf", intf)
                                    
                                    else:
                                        
                                        intf = cfg[(1,0)]
                                        self.cyIO.setInfo("intf", intf)
                                    
                                    """
                                    detail_info = None
                                    intf = cfg[(0,0)]
                                    while 1:
                                        detail_info = list(self.device.ctrl_transfer(0xA1, 0x01, 0x0100, 0, 32))
                                        mirror.text(str(detail_info))
                                        data = ""
                                        data = self.device.read(0x02, 32, 1000)
                                        if data != "":
                                            mirror.text(">>>" + str(list(data)))
                                        #time.sleep(.1)
                                    """
                                    
                                    while detail_info == None:
                                        
                                        if product == 'EPOC+':
                                            detail_info = list(self.device.ctrl_transfer(0xA1, 0x01, 0x0100, 0, 32))
                                        else:
                                            detail_info = list(self.device.ctrl_transfer(0xA1, 0x01, 0x0300, 1, 31))
                                        
                                        if detail_info == None: 
                                            continue
                                        device_firmware   = "0x" + str(hex(detail_info[2]))[2:] +  str(hex(detail_info[3])[2:])
                                        software_firmware = "0x" + str(hex(detail_info[4]))[2:] +  str(hex(detail_info[5])[2:])
                                    
                                    if eval(self.cyIO.getInfo("verbose")) == True:
                                        mirror.text(str(list(detail_info)))
                                        mirror.text(" Device Firmware = "       + device_firmware)
                                        mirror.text(" Software Firmware = "     + software_firmware)
                                        
                                    self.serial_number = str(cyPyUSB.util.get_string(self.device, self.device.iSerialNumber))
                                    self.product_name = str(cyPyUSB.util.get_string(self.device, select_device.iProduct))
                                if eval(self.cyIO.getInfo("verbose")) == True:
                                    mirror.text("> Using Device: " + self.product_name + "\r\n")
                                    mirror.text(" ░░ Serial Number: " + self.serial_number + " ░░\r\n") 
                
            except Exception as e:
                mirror.text(" eegThread.run() Error Communicating With USB. " + str(e))
                os._exit(0)
        
        
        if devicesUsed == 0:
            mirror.text("\r\n> No USB Device Available. Exiting . . . \r\n")
            os._exit(0)
        
        self.cyIO.setInfo("DeviceObject", self.device)
        self.cyIO.setInfo("device",       self.product_name)
        self.cyIO.setInfo("deviceFirmware",  device_firmware)
        self.cyIO.setInfo("softFirmware",    software_firmware)
        
        if eeg_driver == "bluetooth":
            self.cyIO.setInfo("serial",   str(BT_key))
        else:
            self.cyIO.setInfo("serial",   self.serial_number)
        
        if self.product_name == 'EPOC+':
            settings_menu(self.device , self.cyIO, intf);
            return ""
        sn = bytearray()

        for i in range(0,len(self.serial_number)):
            if eeg_driver == "bluetooth":
                sn += bytearray([self.serial_number[i]])
            else:
                sn += bytearray([ord(self.serial_number[i])])
            
        
        if len(sn) != 16:
            return           
            
        k = ['\0'] * 16        
        
        # --- Model 1 > [Epoc::Premium]
        if model == 1:
            k = [sn[-1],00,sn[-2],72,sn[-1],00,sn[-2],84,sn[-3],16,sn[-4],66,sn[-3],00,sn[-4],80]
            self.samplingRate = 128
            self.channels = 40
            
        # --- Model 2 > [Epoc::Consumer]
        if model == 2:   
            k = [sn[-1],00,sn[-2],84,sn[-3],16,sn[-4],66,sn[-1],00,sn[-2],72,sn[-3],00,sn[-4],80]
            self.samplingRate = 128
            self.channels = 40
            
        # --- Model 3 >  [Insight::Premium]
        if model == 3:
            k = [sn[-2],00,sn[-1],68,sn[-2],00,sn[-1],12,sn[-4],00,sn[-3],21,sn[-4],00,sn[-3],88]
            self.samplingRate = 128
            self.channels = 20
            
        # --- Model 4 > [Insight::Consumer]
        if model == 4: 
            k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]
            self.samplingRate = 128
            self.channels = 20
            
        # --- Model 5 > [Epoc+::Premium]
        if model == 5:
            k = [sn[-2],sn[-1],sn[-2],sn[-1],sn[-3],sn[-4],sn[-3],sn[-4],sn[-4],sn[-3],sn[-4],sn[-3],sn[-1],sn[-2],sn[-1],sn[-2]]
            self.samplingRate = 256
            self.channels = 40
            
        # --- Model 6 >  [Epoc+::Consumer]
        if model == 6:
            k = [sn[-1],sn[-2],sn[-2],sn[-3],sn[-3],sn[-3],sn[-2],sn[-4],sn[-1],sn[-4],sn[-2],sn[-2],sn[-4],sn[-4],sn[-2],sn[-1]]
            self.samplingRate = 256
            self.channels = 40
        
        # --- Model 7 > [EPOC+::Standard]-(14-bit mode)
        if model == 7: 
            k = [sn[-1],00,sn[-2],21,sn[-3],00,sn[-4],12,sn[-3],00,sn[-2],68,sn[-1],00,sn[-2],88]
            self.samplingRate = 128
            self.channels = 40

            # 1223332414224421
        #  Set Sampling/Channels Specific to Headset.
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        self.cyIO.setInfo("sampling",str(self.samplingRate))
        self.cyIO.setInfo("channels",str(self.channels))
        self.cyIO.setInfo("keymodel",str(model))
        
        if eeg_driver == "bluetooth":
            return bytes(bytearray(k))
        
        if eval(self.cyIO.getInfo("verbose")) == True:
            mirror.text("═" *90)
            mirror.text("   AES Key = " + str(k))
        return k
        
    #  PyWinUSB (/cyUSB) Raw Data Handler. Thread.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def dataHandler(self, data):
        
       
        if eeg_driver == "pyusb":
            return
        try:
            if self.outputraw == True:
                mirror.text(str(list(data)))
        except:
            pass
        join_data = ''.join(map(chr, data[1:]))
        tasks.put(join_data)
        # Note: PyWinUSB receives 33 bytes of data. First byte is always 0.
        return True

    #  (Epoc / Insight) Data Conversion.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def convertEPOC(self, data, bits):
        
       
        level = 0
        for i in range(13, -1, -1):
            
            level <<= 1
            b = int((bits[i] / 8) + 0) # Added int() getting floats?
            o = bits[i] % 8
            level |= (data[b] >> o) & 1
        return level
    
    #  (Epoc+) Data Conversion.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def convertEPOC_PLUS(self, value_1, value_2):
        
       
        edk_value = "%.8f" % (((int(value_1) * .128205128205129) + 4201.02564096001) + ((int(value_2) -128) * 32.82051289))
        if self.integer == True:
            return str(int(float(edk_value)))
        return edk_value
         
    #  eegThread. (Thread Start).
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    def run(self, key, cyIO):       
        
        
        #  Display Active Python Process Threads.
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        if eval(cyIO.getInfo("verbose")) == True:
            t_array = str(list(map(lambda x: x.getName(), threading.enumerate())))
            mirror.text("\r\nActive Threads = {")
            mirror.text("   " + t_array)
            mirror.text("} \r\n")
                    
        cyIO.setBaselineMode(self.baseline)
        while eval(cyIO.getInfo("status")) != True:
            
            time.sleep(0)
            pass
            
        tasks.queue.clear()

        #  Bypass Sending Header Data.
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        if eval(cyIO.getInfo("noheader")) == False:

            #  Connected. Send Device Header to Data Stream.
            # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
            if eval(cyIO.getInfo("status")) == True and eval(cyIO.getInfo("noweb")) == False:
                cyIO.sendInfo("device")
                cyIO.sendInfo("serial")

                firmware = cyIO.getInfo("softFirmware")[2:5]          # Auto-Detect firmware for EPOC+
                if int(firmware[0]) ==  6:
                    cyIO.sendData(1,"CyKITv2:::Info:::keymodel:::6")
                else:
                    cyIO.sendInfo("keymodel")

                cyIO.sendInfo("config")
                cyIO.sendInfo("datamode")
                cyIO.sendData(1,"CyKITv2:::Info:::delimiter:::" + str(ord(cyIO.getInfo("delimiter"))))
                
                    
                
        self.generic = cyIO.getInfo("generic")

        #  Update Local Variables from ControllerIO Dictionary.
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        
        for index in self.configFlags:
            setattr(self, index, eval(cyIO.getInfo(index)))
                            
        #  EPOC+ Mode. (Direct USB Connection)
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        if key == "":
            while self.running:
                time.sleep(0)
                
                if eval(cyIO.getInfo("status")) != True:
                    time.sleep(0)
                    self.running = False
                    continue
            return
        AES_key = key       

        #  Create AES(ECB) Cipher.
        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        try:
            if eeg_driver == "bluetooth":
                pass
            else:
                AES_key = bytes(bytearray(key))
            
            if eval(cyIO.getInfo("verbose")) == True:
                mirror.text(" Cipher Key = "  + str(key))
            
            cipher = AES.new(AES_key, AES.MODE_ECB)

        except Exception as exception:
            mirror.text( " eegThread.run() : E1. Failed to Create AES Cipher ::: " + (str(exception)))
        
        while self.running:
            time.sleep(0)
            
            if eval(cyIO.getInfo("status")) != True:
                time.sleep(0)
                self.running = False
                continue

                if eeg_driver == "pywinusb":
                    t_array = str(list(map(lambda x: x.getName(), threading.enumerate())))
                    while "Thread-" in t_array:
                        time.sleep(0)
                        t_array = str(list(map(lambda x: x.getName(), threading.enumerate())))
                        cyIO.getInfo("DeviceObject").set_raw_data_handler(None)
                        cyIO.getInfo("DeviceObject").close()
                    continue

            if self.blankdata == True:
                try:
                    if self.blank_data[self.KeyModel] == None:
                        mirror.text(" ¯¯¯¯ No 'blankdata' for this model. Disabling 'blankdata' Mode.")
                        self.blankdata = False
                        return
                    data = self.blank_data[self.KeyModel]
                    join_data = ''.join(map(chr, data))
                    time.sleep(0) # Slow it down.
                    encrypted_blank_cipher = b"0" + (cipher.encrypt(bytes(join_data,'latin-1')))               
                except Exception as e:
                    mirror.text(" ¯¯¯¯ eegThread.run() Failed to Create Blank Cipher. Disabling 'blankdata' Mode.")
                    mirror.text(" =E.4: " + str(e))
                    self.blankdata = False
                    return

                if eeg_driver == "pywinusb":
                    self.dataHandler(encrypted_blank_cipher)
                    
                if eeg_driver == "pyusb":
                    tasks.put(encrypted_blank_cipher[1:])
                
            if eeg_driver == "pyusb" and self.blankdata == False:
                
                try:
                    
                    #task = self.device.read(0x00, 32, 100)
                    #mirror.text(str(list(task))
                    # 0x60
                    task = self.device.read(0x82, 32, 100)
                    tasks.put(task.tobytes())
                    
                except Exception as e:
                    
                    #Read Timeout. (Device Not Turned On.)
                    if e.errno == 10060:
                        if 'dataLoss' not in locals():
                            dataLoss = 0
                        dataLoss += 1
                        # 10 Failed Reads. (Device Turned Off.)
                        if dataLoss > 50:
                            mirror.text("\r\n ░░░ Device Interference or Turned Off ░░░ \r\n")
                            if cyIO.isRecording() == True:
                                cyIO.stopRecord()
                            if eval(cyIO.getInfo("noheader")) == False:
                                cyIO.sendData(1, "CyKITv2:::noData")
                            cyIO.setInfo("status","False")
                            cyIO.onClose("dataLoss")
                        continue

                    # USB Disconnect. I/O Error.
                    if e.errno == 5:
                        mirror.text("Error Finding USB Device.")
                        os._exit(0)
                    mirror.text("OSError.eeg = " + str(e.errno))
                    exc_type, ex, tb = sys.exc_info()
                    imported_tb_info = traceback.extract_tb(tb)[-1]
                    line_number = imported_tb_info[1]
                    print_format = "{}: Exception in line: {}, message: {}"
                    mirror.text(" ¯¯¯¯¯ eegThread.run() Error reading data.")
                    mirror.text(" =E.11: " + print_format.format(exc_type.__name__, line_number, ex))
            
            sleep_time = time.time()
            dataLoss = 0

            while not tasks.empty() and self.running == True:
                time.sleep(0)

                if eeg_driver == "pyusb":
                    dbg.txt("eeg() -- pyusb ")
                    if self.blankdata == False:
                        try:
                            task = self.device.read(0x82, 32, 500)
                            tasks.put(task.tobytes())
                        except Exception as e:
                            if str(e.errno) != "10060":
                                mirror.text("Error.eeg() = " + str(e.errno))
                                exc_type, ex, tb = sys.exc_info()
                                imported_tb_info = traceback.extract_tb(tb)[-1]
                                line_number = imported_tb_info[1]
                                print_format = "{}: Exception in line: {}, message: {}"
                            if 'dataLoss' not in locals():
                                dataLoss = 0
                            dataLoss += 1
                            if dataLoss > 50:
                                mirror.text("\r\n ░░░ Device Interference or Turned Off ░░░ \r\n")
                                if cyIO.isRecording() == True:
                                    cyIO.stopRecord()
                    else:
                        time.sleep(0)
                        tasks.put(encrypted_blank_cipher[1:])

                #  Update Run-Time Config Options.
                # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                check_mask = cyIO.maskChange()
                self.format = int(cyIO.getInfo("format"))
                self.datamode = int(cyIO.getInfo("datamode"))
                self.delimiter = cyIO.getInfo("delimiter")
                self.baseline = eval(cyIO.getInfo("baselinemode"))

                if check_mask != None:
                    self.mask[check_mask] = cyIO.getMask(check_mask)
                    mirror.text(self.mask[check_mask])

                try:

                    counter_data = ""
                    packet_data = ""
                    filter_data = ""
                    
                    if eeg_driver == "bluetooth":
                        task = tasks.get()
                        decrypted = cipher.decrypt(task[0:16])
                        sel_decrypt = decrypted[0:1] + decrypted[1:16]
                        if BTLE_device_name == "Insight":
                            data = task[19:20]  \
                            + sel_decrypt \
                            + task[16:17] \
                            + task[17:18] \
                            + task[18:19]

                        else:
                            try:
                                data = cipher.decrypt(task)
                            except:
                                return
                                
                        
                        if self.outputraw == True:
                            mirror.text(str(list(task)))
                        if self.outputdata == True:
                            mirror.text(str(list(data)))
                        
                    if eeg_driver == "pywinusb":
                        task = tasks.get()
                        data = cipher.decrypt(bytes(task,'latin-1')[0:32])
                        #data = cipher.decrypt(task[0:32])
                        
                    if eeg_driver == "pyusb":
                        task = tasks.get()
                        data = cipher.decrypt(task)
                        if self.outputraw == True:
                            mirror.text(str(list(task)))
                    
                    # Function Every Second. 
                    if (int(time.time() % 60) - self.getSeconds) == 1:
                        time.sleep(0)
                        if eval(cyIO.getInfo("status")) != True:
                            self.running = False

                            t_array = str(list(map(lambda x: x.getName(), threading.enumerate())))
                            while "Thread-" in t_array:
                                time.sleep(0)
                                threadMax = 0
                                t_array = str(list(map(lambda x: x.getName(), threading.enumerate())))
                                mirror.text(t_array)
                                self.cyIO.getInfo("DeviceObject").set_raw_data_handler(None)
                                self.cyIO.getInfo("DeviceObject").close()
                            continue
                    
                    self.getSeconds = int(time.time() % 60)

                    #  Epoc. 
                    # ¯¯¯¯¯¯¯¯
                    if self.KeyModel == 2 or self.KeyModel == 1:
                        
                        if self.nocounter == True:
                            counter_data = ""
                        else:
                            counter_data = str(data[0]) + self.delimiter
                        
                        # +Format-0: (Default) 
                        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        if self.format < 1:
                            for i in range(0,14):
                                packet_data = packet_data + str(self.convertEPOC(data[1:], self.mask[i])) + self.delimiter
                            packet_data = packet_data[:-len(self.delimiter)] # Remove extra delimiter.
                            if cyIO.isRecording() == True:
                                cyIO.startRecord(counter_data + packet_data)
                            if self.outputdata == True:
                                mirror.text(str(counter_data + packet_data))
                        
                        
                        # +Format-1: Raw Data (Data Not Decoded)
                        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        if self.format == 1:
                            for i in range(1, len(data)):
                                packet_data = packet_data + str(data[i]) + self.delimiter
                            packet_data = packet_data[:-len(self.delimiter)] # Remove extra delimiter.
                            if cyIO.isRecording() == True:
                                cyIO.startRecord(counter_data + packet_data)
                            if self.outputdata == True:
                                mirror.text(str(counter_data + packet_data))
                    
                        # +Format-3: Decode for 2015 EPOC+ firmware.  [Not complete for gyro format]
                        # ----------------------------------------------------------------------------
                        if self.format == 3:
                            
                            if self.nocounter == True:
                                counter_data = ""
                            else:
                                counter_data = str(data[0]) + self.delimiter + "16" + self.delimiter
                                
                            z = ''
                            for i in range(1, len(data)):
                                z = z + format(data[i],'08b')
                                
                            for i in range(2, len(self.insight_1),2):
                                i_1 = self.insight_1[(i-2)]
                                i_2 = self.insight_1[(i-1)]
                            
                                if i_2 > len(z):
                                    i = len(self.insight_1)
                                    continue

                                v_1 = '0b' + z[(i_1):(i_2)]
                                v_2 = '0b' + z[(i_2):(i_2+6)]

                                if i == 16 or i == 18:
                                    data_line = str(int(eval(v_1))) + self.delimiter + str(int(eval(v_2)))
                                    continue

                                packet_data = packet_data + self.convertEPOC_PLUS(str(int(eval(v_2))), str(int(eval(v_1)))) + self.delimiter
                            
                            if self.nobattery == False:
                                packet_data += data_line                          # Append data lines for battery and quality.
                            else:
                                packet_data = packet_data[:-len(self.delimiter)]  # Remove extra delimiter.
                            
                            if self.outputdata == True:
                                print(counter_data + packet_data)

                            if cyIO.isRecording() == True:
                                cyIO.startRecord(counter_data + packet_data)


                    
                    #eval('0xaf0faf') >> (14*1+1) & 0b1111111
                    #  Insight.
                    # ¯¯¯¯¯¯¯¯¯¯¯
                    if self.KeyModel == 4 or self.KeyModel == 7:

                        if self.nocounter == True:
                            counter_data = ""
                        else:
                            counter_data = str(data[0]) + self.delimiter
                            
                        # ~Format-0: (Default) (Decodes to Floating Point) 
                        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        
                        if self.format == 2: 
                            
                            z = ''
                            for i in range(1,len(data)):
                                z = z + format(data[i],'08b')
                            
                            for i in range(2,len(self.insight_1),2):
                                i_1 = self.insight_1[(i-2)]
                                i_2 = self.insight_1[(i-1)]
                                
                                #mirror.text(str(i_1) + ":" + str(i_2))
                                
                                if i_2 > len(z):
                                    i = len(self.insight_1)
                                    continue
                                # Get 2 halves of 14bytes (8byte + 6byte)
                                v_1 = '0b' + z[(i_1):(i_2)]
                                v_2 = '0b' + z[(i_2):(i_2+6)]
                                
                                packet_data = packet_data + str(int(eval(v_1))) + self.delimiter + str(int(eval(v_2))) + self.delimiter
                            
                            packet_data = packet_data[:-len(self.delimiter)] # Remove extra delimter

                        #Bluetooth Formatting.
                        if self.format == 3:                           
                            # Every 14 Bits of first 10 Bytes are split up into 8 bit + 6 bits.
                            
                            bit_array = []
                            c_bits = ''.join(list(map(lambda x: format(x, '08b'), data[1:])))

                            for i in range(0, int(len(c_bits)), 14):
                                bits_8 = '0b' + c_bits[i:i+8]
                                bits_6 = '0b' + c_bits[i+8:i+13]
                                bit_array.append(int(eval(bits_8)))
                                bit_array.append(int(eval(bits_6)))
                            
                            packet_data = str(bit_array)[:-1][1:]
                            
                        if self.format < 1:
                            for i in range(1,16,2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter
                            
                            for i in range(18,len(data),2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

                            packet_data = packet_data[:-len(self.delimiter)]
                            """ Insight not currently supported for openvibe.  
                                Will need to select the channels necessary. Will update in next revision.
                            if self.openvibe == True and self.nocounter == True:
                                ov_data = [float(x) for x in packet_data.split(self.delimiter)][0:5]
                                ov_data = str(ov_data)
                                ov_data = ov_data[1:]
                                ov_data = ov_data[:-1]
                                packet_data = str(ov_data)
                                print(str(ov_data))
                            """                         
                            if self.nobattery == False:
                                packet_data = packet_data + self.delimiter + str(data[16]) + str(self.delimiter) + str(data[17]) 
                                
                        #  ~Format-1: (Raw Data Format.) (Data not Decoded)
                        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        if self.format == 1: 
                            for i in range(1,len(data)):
                                packet_data = packet_data + str(data[i]) + self.delimiter
                            packet_data = packet_data[:-len(self.delimiter)]

                        if self.outputdata == True:
                            mirror.text(str(counter_data + packet_data))
                        if cyIO.isRecording() == True:
                            cyIO.startRecord(counter_data + packet_data)
                        
                    #  Epoc+
                    # ¯¯¯¯¯¯¯¯
                    if self.KeyModel == 6 or self.KeyModel == 5:

                        if str(data[1]) == "16":
                            if self.datamode == 2:
                                continue

                        if str(data[1]) == "32":
                            self.format = 1
                            if self.datamode == 1:
                                continue

                        if self.nocounter == True:
                            counter_data = ""
                        else:
                            counter_data = str(data[0]) + self.delimiter + str(data[1]) + self.delimiter

                        # ~Format 0: (Default) (Decode to Floating Point)
                        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        if self.format < 1:
                            for i in range(2,16,2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

                            for i in range(18,len(data),2):
                                packet_data = packet_data + str(self.convertEPOC_PLUS(str(data[i]), str(data[i+1]))) + self.delimiter

                            packet_data = packet_data[:-len(self.delimiter)] # Remove extra delimiter.

                            #  Averages Signal Data and Sends to Client.
                            # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

                            if self.baseline == True:
                                
                                if (int(time.time() % 60) - self.baseSeconds) == 1:  # Baseline Every Second.
                                    #mirror.text("BASELINE ¯¯¯¯¯¯¯ " + str(self.baseline))
                                    try:
                                        if 'baseline_values' in locals():
                                            baseline_last = baseline_values
                                        baseline_values = [float(x) for x in packet_data.split(self.delimiter)]

                                        if baseline_values != None and 'baseline_last' in locals():
                                            baseline_values = list(map(operator.add, baseline_last, baseline_values))
                                            set_values = ([2] * len(baseline_values))
                                            baseline_values = list(map(operator.truediv, baseline_values, set_values))

                                            #  Re-order values.
                                            # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                                            # self.epocOrder = [2,3,0,1,4,5,6,7,8,9,12,13,10,11]
                                            #baseline_new = [baseline_values[i] for i in self.epocOrder]

                                            cyIO.setBaseline(baseline_values)
                                            
                                            send_baseline = [0.0,float(str(data[1]))] + baseline_values
                                            
                                            send_baseline = str(send_baseline)
                                            
                                            send_baseline = send_baseline[1:]
                                            
                                            send_baseline = send_baseline[:(len(send_baseline)-1)]
                                            if self.outputdata == True:
                                                mirror.text("Python Baseline:::")
                                                mirror.text(str(send_baseline))
                                            
                                            cyIO.sendData(1, "CyKITv2:::Baseline:::" + str(send_baseline))
                                    
                                    except Exception as e:
                                        exc_type, ex, tb = sys.exc_info()
                                        imported_tb_info = traceback.extract_tb(tb)[-1]
                                        line_number = imported_tb_info[1]
                                        print_format = "{}: Exception in line: {}, message: {}"
                                        mirror.text(" ¯¯¯¯ eegThread.run() Error Creating Baseline Data.")
                                        mirror.text(" =E.7: " + print_format.format(exc_type.__name__, line_number, ex))    
                                self.baseSeconds = int(time.time() % 60)
                            
                            #  Contact Quality. RMS Value.
                            # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                            #if self.quality == True:
                            #baseline_values = map(math.sqrt, baseline_values)

                            if self.nobattery == False:
                                    packet_data = packet_data + self.delimiter + str(data[16]) + str(self.delimiter) + str(data[17]) 

                            if cyIO.isRecording() == True:
                                record_data = packet_data
                                if self.blankcsv == True:
                                    emptyCSV = ("0" + self.delimiter) * int(self.channels - (16 + abs((self.nobattery & 1) *-2)))

                                    emptyCSV = emptyCSV[:-2]
                                    record_data = packet_data + self.delimiter + emptyCSV
                                cyIO.startRecord(counter_data + record_data)

                            if self.outputdata == True:
                                mirror.text(str(counter_data + packet_data))

                        #  ~Format-1: (Raw Data Format.) (Data not Decoded)
                        # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        if self.format == 1:
                                for i in range(2,16,2):
                                    packet_data = packet_data + str(data[i]) + self.delimiter + str(data[i+1]) + self.delimiter

                                for i in range(18,len(data),2):
                                    packet_data = packet_data + str(data[i]) + self.delimiter + str(data[i+1]) + self.delimiter

                                packet_data = packet_data[:-len(self.delimiter)]
                                
                                if cyIO.isRecording() == True:
                                    cyIO.startRecord(counter_data + packet_data)

                                if self.nobattery == False:
                                    packet_data = packet_data + self.delimiter + str(data[16]) + self.delimiter + str(data[17]) 

                                if self.outputdata == True:
                                    mirror.text(str(counter_data + packet_data))
                    try:
                        if self.openvibe == True:
                            if self.integer == True:
                                cyIO.sendOVint(counter_data + packet_data)
                            else:
                                cyIO.sendOVfloat(counter_data + packet_data)
                            
                        else:
                            if self.filter == True and self.format == 0:
                                if 'baseline_values' in locals():
                                    mirror.text(str("Baseline:"))
                                    mirror.text(str(packet_data))
                                    if self.nocounter == False:
                                        split_packet = packet_data.split(self.delimiter)
                                        split_packet = split_packet[:-2]
                                    else:
                                        split_packet = packet_data.split(self.delimiter)
                                        
                                    
                                    convert_packet = [float(x) for x in split_packet]
                                    filter_data = map(operator.sub, baseline_values, convert_packet)
                                    mirror.text(str("subtract::"))
                                    mirror.text(str(convert_packet))
                                    packet_data = str(filter_data)
                                    packet_data = packet_data[1:]
                                    packet_data = packet_data[:(len(packet_data)-1)]
                            
                            self.cyIO.sendData(1, counter_data + packet_data)

                    except OSError as e:
                        error_info = str(e.errno)
                        if error_info == "10035":
                            self.time_delay += .001
                            time.sleep(self.time_delay)
                            continue
                            
                        if error_info == 9 or error_info == 10053 or error_info == 10035 or error_info == 10054:
                            mirror.text("EEG() E.4" + str(msg))
                            mirror.text("\r\n Connection Closing.\r\n")
                            
                            tasks.queue.clear()
                            if self.generic == True:
                                cyIO.onClose("0")
                            else:
                                cyIO.onClose("1")
                                if eeg_driver == "pywinusb":
                                    self.device.close()
                                cyIO.stopRecord()
                            continue
                        mirror.text(" ¯¯¯¯ eegThread.run() Error creating OpenVibe Data and or Filtering Data.")
                        mirror.text(" =E.10: " + str(msg))

                except Exception as e:
                    exc_type, ex, tb = sys.exc_info()
                    imported_tb_info = traceback.extract_tb(tb)[-1]
                    line_number = imported_tb_info[1]
                    print_format = "{}: Exception in line: {}, message: {}"
                    mirror.text(" ¯¯¯¯ eegThread.run() Error Formatting Data.")
                    mirror.text(" =E.8: " + print_format.format(exc_type.__name__, line_number, ex))    
