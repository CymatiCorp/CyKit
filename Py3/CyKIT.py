# -*- coding: utf8 -*-
#
#  CyKIT   2018.Dec.27
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
#  CyKIT.py 
#  Written by Warren
# 
#  Launcher to initiate EEG setup.
#  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

import os
import sys
import socket
import select
import struct
import eeg
import CyWebSocket
import threading
import time
import traceback
import inspect
    
arg_count = len(sys.argv)

def mirror(custom_string):
        try:
            print(str(custom_string))
            return
        except OSError as exp:
            return

if arg_count == 1 or arg_count > 5 or sys.argv[1] == "help" or sys.argv[1] == "--help" or sys.argv[1] == "/?":
    mirror("\r\n")
    mirror(" (Version: CyKIT 3.0:2018.Dec.26) for Python 3.x on (Win32 or Win64) \r\n")
    mirror("\r\n Usage:  Python.exe .\\CyKIT.py <IP> <Port> <Model#(1-6)> [config] \r\n\r\n")
    mirror(" Must be launched from the CyKIT directory, do not use py launcher.\r\n")
    mirror(" " + "═" * 100 + "\r\n")
    mirror(" <IP> <PORT> for CyKIT to listen on. \r\n")
    mirror(" " + ("═" * 100) + "\r\n")
    mirror(" <Model#> Choose the decryption type. \r\n")
    mirror("          1 - Epoc    (Premium  Model)\r\n")
    mirror("          2 - Epoc    (Consumer Model)\r\n")
    mirror("          3 - Insight (Premium  Model)\r\n")
    mirror("          4 - Insight (Consumer Model) \r\n")
    mirror("          5 - Epoc+   (Premium  Model)\r\n")
    mirror("          6 - Epoc+   (Consumer Model) [16-bit EPOC+ mode] \r\n\r\n")
    mirror("          7 - EPOC+   (Consumer Model) [14-bit EPOC  mode] \r\n")
    mirror(" " + "═" * 100 + "\r\n")
    mirror(" [config] is optional. \r\n")
    mirror("  'info'                Prints additional information into console.\r\n\r\n")
    mirror("  'confirm'             Requests you to confirm a device everytime device is initialized.\r\n\r\n")
    mirror("  'verbose'             Prints extra information regarding the inner workings of CyKIT.\r\n\r\n")
    mirror("  'nocounter'           Removes COUNTER and INTERPOLATE from outputs. (Must also use either nogyro or noeeg) \r\n")
    mirror("                         (nogyro is enabled by default.) This ensures streams are differentiated. \r\n\r\n")
    mirror("  'noheader'            Removes CyKITv2::: header information. (Required for openvibe) \r\n\r\n")
    mirror("  'format-0'            (Default) Outputs 14 data channels in float format. ('4201.02564096') \r\n\r\n")
    mirror("  'format-1'            Outputs the raw data (to be converted by Javascript or other). \r\n\r\n")
    mirror("  'format-3'            Used only with Insight(USB), selects specific bit ranges to acquire data.\r\n\r\n")
    mirror("  'outputdata'          Prints the (formatted) data being sent, to the console window.\r\n\r\n")
    mirror("  'outputraw'           Prints the (encrypted) rjindael data to the console window.\r\n\r\n")
    mirror("  'blankdata'           Injects a single line of encrypted data into the stream that is \r\n")
    mirror("                         consistent with a blank EEG signal. Counter will report 0. \r\n\r\n")
    mirror("  'blancsv'             Adds blank channels for each CSV line, to be used with logging.\r\n\r\n")
    mirror("  'generic'             Connects to any generic program via TCP. (Can be used with other flags.)\r\n\r\n")
    mirror("  'openvibe'            Connects to the generic OpenViBE Acquisition Server.\r\n\r\n")
    mirror("                         must use generic+nocounter+noheader+nobattery Other flags are optional.\r\n")
    mirror("  'ovdelay'             Stream sending delay. (999 maximum) Works as a multiplier, in the format: ovdelay:001 \r\n\r\n")
    mirror("  'ovsamples'           Changes openvibe sample rate. Format: ovsamples:001 \r\n\r\n")
    mirror("  'integer'             Changes format from float to integer. Works with other flags. Including openvibe. \r\n\r\n")
    mirror("  'baseline'            Averages data and sends the baseline value to socket.\r\n\r\n")
    mirror("  'path'                Prints the Python paths used to acquire modules.\r\n\r\n")
    mirror("  'filter'              When used with baseline, subtracts the data value from baseline and sends to sockets.\r\n\r\n")
    mirror("  'allmode'             Sends Gyro and EEG data packets (Can change during run-time)\r\n\r\n")
    mirror("  'eegmode'             Sends only EEG packets. (Can change during run-time)\r\n\r\n")
    mirror("  'gyromode'            Sends only Gyro packet. (Can change during run-time)\r\n\r\n")
    mirror("  'pywinusb'            Specifies to use the pywinusb libraries to connect to the USB device.\r\n\r\n")
    mirror("                         Defaults to using libusb libraries.\r\n\r\n")
    mirror("  'noweb'               Displays data. (without requiring a TCP connection.)\r\n\r\n")
    mirror("  'bluetooth'  Attempt to AUTO-DETECT an already paired bluetooth device.\r\n\r\n")
    mirror("  'bluetooth=xxxxxxxx'  Connect to an already paired bluetooth device, use the hex digit found in the devices pairing name.\r\n\r\n")
    mirror("                         The pairing name can easily be found in Windows Bluetooth settings.\r\n\r\n")
    mirror("   Join these options (in any order), using a + separator. \r\n")
    mirror("   (e.g  info+confirm ) \r\n\r\n")
    mirror(" " + "═" * 100 + "\r\n")
    mirror("  Example Usage: \r\n")
    mirror("  Python.exe .\\CyKIT.py 127.0.0.1 54123 1 info+confirm \r\n\r\n")
    mirror("  Example Usage: \r\n")
    mirror("  Python.exe .\\CyKIT.py 127.0.0.1 5555 6 openvibe+generic+nocounter+noheader+nobattery+ovdelay:100+integer+ovsamples:004 \r\n\r\n")
    mirror(" " + "═" * 100 + "\r\n")
    sys.argv = [sys.argv[0], "127.0.0.1", "54123", "1", ""]
    
    
if arg_count < 5:
    
    if arg_count == 2:
        sys.argv = [sys.argv[0], sys.argv[1], "54123", "1", ""]
    if arg_count == 3:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], "1", ""]
    if arg_count == 4:
        sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3], ""]

if sys.argv[2].isdigit() == False or int(sys.argv[2]) < 1025 or int(sys.argv[2])> 65535:
    mirror("Invalid Port #[" + str(sys.argv[2]) + "] (Must be a local port in range: 1025 - 65535)")
    os._exit(0)

if sys.argv[3].isdigit() == False:
    mirror("Invalid Key # [" + str(sys.argv[3]) + "] (Must be a numeric 1 - 9)")
    os._exit(0)

if int(sys.argv[3]) < 1 or int(sys.argv[3]) > 9:
    mirror("Invalid Key # [" + str(sys.argv[2]) + "] (Must be a numeric 1-9)")
    os._exit(0)


def main(CyINIT):

    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])
    MODEL = int(sys.argv[3])
    check_connection = None
    parameters = str(sys.argv[4]).lower()

    #  Stage 1.
    # ¯¯¯¯¯¯¯¯¯¯¯
    #  Acquire I/O Object.
    # ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    cy_IO = eeg.ControllerIO()
    
    cy_IO.setInfo("ioObject", cy_IO)
    cy_IO.setInfo("config", parameters)

    if "verbose" in parameters: 
        cy_IO.setInfo("verbose","True")
    else:                   
        cy_IO.setInfo("verbose","False")

    if "noweb" in parameters:
        noweb = True
        cy_IO.setInfo("noweb","True")
        cy_IO.setInfo("status","True")
    else:
        noweb = False
        cy_IO.setInfo("noweb","False")
    
    if "noheader" in parameters:
        cy_IO.setInfo("noheader","True")

    if "openvibe" in parameters:
        cy_IO.setInfo("openvibe","True")


    headset = eeg.EEG(MODEL, cy_IO, parameters)
    
    while str(cy_IO.getInfo("DeviceObject")) == "0":
        time.sleep(.001)
        continue
    
    if "bluetooth" in parameters:
            mirror("> [Bluetooth] Pairing Device . . .")
    else:
        if "noweb" not in parameters:
            mirror("> Listening on " + HOST + " : " + str(PORT))

    mirror("> Trying Key Model #: " + str(MODEL))

    if "generic" in parameters:
        ioTHREAD = CyWebSocket.socketIO(PORT, 0, cy_IO)
    else:
        ioTHREAD = CyWebSocket.socketIO(PORT, 1, cy_IO)
    
    cy_IO.setServer(ioTHREAD)
    time.sleep(1)
    check_connection = ioTHREAD.Connect()
    ioTHREAD.start()
    
    while eval(cy_IO.getInfo("status")) != True:
        time.sleep(.001)
        continue   
    
    headset.start()
    
    if eval(cy_IO.getInfo("openvibe")) == True:
        time.sleep(3)
    
    CyINIT = 3
        
    while CyINIT > 2:
        
        CyINIT += 1
        time.sleep(.001)
        
        if (CyINIT % 10) == 0:
            

            check_threads = 0
            
            t_array = str(list(map(lambda x: x.name, threading.enumerate())))
            #if eval(cy_IO.getInfo("verbose")) == True:
            #    mirror(" Active Threads :{ " + str(t_array) + " } ")
            #time.sleep(15)
            
            if 'ioThread' in t_array:
                check_threads += 1
                
            if 'eegThread' in t_array:
                check_threads += 1

            if eval(cy_IO.getInfo("openvibe")) == True:
                if check_threads == 0:
                    ioTHREAD.onClose("CyKIT.main() 2")
                    mirror("\r\n*** Reseting . . .")
                    CyINIT = 1
                    main(1)
                continue
            
            #(1 if noweb == True else 2)
            
            if check_threads < (1 if noweb == True else 2):
                
                threadMax = 2
                totalTries = 0
                while threadMax > 1 and totalTries < 2:
                    totalTries += 1
                    time.sleep(0)
                    threadMax = 0
                    for t in threading.enumerate():
                        if "eegThread" in t.name:
                            cy_IO.setInfo("status","False")
                            #mirror(t.name)
                        if "ioThread" in t.name:
                            #mirror(t.name)
                            CyWebSocket.socketIO.stopThread(ioTHREAD)
                        
                        if "Thread-" in t.name:
                            #mirror(t.name)
                            threadMax += 1
                            try:
                                t.abort()
                            except:
                                continue
                t_array = str(list(map(lambda x: x.name, threading.enumerate())))
                #mirror(str(t_array))
                ioTHREAD.onClose("CyKIT.main() 1")
                mirror("*** Reseting . . .")
                CyINIT = 1
                main(1)

try:
    try:
        main(1)
    except OSError as exp:
        main(1)

except Exception as e:
    exc_type, ex, tb = sys.exc_info()
    imported_tb_info = traceback.extract_tb(tb)[-1]
    line_number = imported_tb_info[1]
    print_format = '{}: Exception in line: {}, message: {}'
    
    mirror("Error in file: " + str(tb.tb_frame.f_code.co_filename) + " >>> ")
    mirror("CyKITv2.Main() : " + print_format.format(exc_type.__name__, line_number, ex))
    mirror(traceback.format_exc())
    
    mirror(" ) WARNING_) CyKIT2.main E1: " + str(e))
    mirror("Error # " + str(list(OSError)))
    mirror("> Device Time Out or Disconnect . . .  [ Reconnect to Server. ]")
    main(1)
