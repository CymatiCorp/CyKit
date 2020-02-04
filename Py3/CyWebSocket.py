# -*- coding: utf8 -*-
#
#  ♦ CyKIT ♦  2018.Dec.26
# ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
#  CyWebSocket.py 
#  Adapted by Warren
#
#  pywebsocketserver.py
#  Written  by suxianbaozi
#
#  Python web server for connecting sockets locally 
#  with browsers  as well as a generic TCP server.
#

import sys
import socket
import time
import select
import threading
import hashlib
import base64
import struct
import traceback
import inspect

class dbg():
    def txt(custom_string):
        return
        try:
            print(custom_string)
            return
        except OSError as exp:
            return

class mirror():
    def text(custom_string):
        
        try:
            print(str(custom_string))
            return
        except OSError as exp:
            return

class socketIO():
    
    def __init__(self, port, uid, ioHandler):
        self.time_delay = .001
        self.openvibe = False
        self.ovdelay = 100
        self.port = port
        self.con = None
        self.isHandleShake = False
        self.uid = uid
        self.io = ioHandler
        self.signKey = "ADS#@!D"
        self.online = True
        self.generic = False
        self.lock = threading.Lock()
        self.thread_2 = threading.Thread(name='ioThread', target=self.run, daemon=False)
        self.stop_thread = False
        self.ovData = bytes()
        self.ovsamples = 4
        self.ov_packetCount = 0
        self.verbose = False
        self.io.setInfo("generic","False")
        self.verbose = eval(self.io.getInfo("verbose"))
        
        if uid == 0:
            self.io.setInfo("generic","True")
            self.generic = True
            self.isHandleShake = True
        
    def start(self):
        self.socketThreadRunning = True
        self.thread_2.start()

    def Disconnect(self):
        self.socketThreadRunning = False
        self.con.close()
        
    def Connect(self):
        
        if eval(self.io.getInfo("noweb")) == True:
            time.sleep(0)
            return "noweb"
        mirror.text("(-) Connecting . . .")
        
        # Row.  Row.  Row.  Your Boat.  Gently Down The ______
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('',self.port))
        sock.listen(1)

        try:
            (self.con,address) = sock.accept()
            mirror.text("(+) Connected.\r\n")

        except socket.error as e:
            mirror.text("(-) Not Connected. ")
            mirror.text(" Socket Error: " + str(e))

        return self.con

    def stopThread(self):
        self.socketThreadRunning = False
        return

    def run(self):
        self.socketThreadRunning = True
        time.sleep(.001)

        if eval(self.io.getInfo("noweb")) == True:

            time.sleep(.001)
            while self.socketThreadRunning == True:

                if eval(self.io.getInfo("status")) != True:
                    return
                time.sleep(.001)
                continue
            return

        if eval(self.io.getInfo("openvibe")) == True:
                time.sleep(.001)
                self.io.onGeneric(0)
                self.ovdelay = (int(self.io.getInfo("ovdelay")) * 100)
                self.ovsamples = int(self.io.getInfo("ovsamples"))
                
        while self.socketThreadRunning == True:
            time.sleep(.001)
            if eval(self.io.getInfo("openvibe")) == True:
                self.openvibeTimer = 0
                while self.openvibeTimer > self.ovdelay:
                    time.sleep(.001)
                    self.openvibeTimer += 1
                return

            if eval(self.io.getInfo("generic")) == True:
                try:
                    self.con.setblocking(0)
                    ready = select.select([self.con], [], [], 1)
                    if ready[0]:
                        if "closed" in str(self.con):
                            return
                        try:
                            clientData = self.con.recv(1024).decode()
                            if clientData == '':
                                return
                        except:
                            return
                        self.io.onGeneric(0)
                        if eval(self.io.getInfo("openvibe")) == True:
                            self.openvibe = True
                        continue
                    continue
                except socket.error as e:
                    mirror.text(" ==== CyWebSocket().run() - (Generic TCP) ")
                    mirror.text(str(socket.error))
                    if e.errno == 10035:
                        self.time_delay += .001
                        time.sleep(self.time_delay)
                        return
                    return

            if not self.isHandleShake: 
                try:
                    self.con.setblocking(0)
                    ready = select.select([self.con], [], [], 1)
                    if ready[0]:
                        if "closed" in str(self.con):
                            return
                        try:
                            clientData  = self.con.recv(1024).decode()
                        except:
                            return
                        if clientData == '':
                            return
                        dataList = clientData.split("\r\n")
                        header = {}
                        
                        for data in dataList:
                            if ": " in data:
                                unit = data.split(": ")
                                header[unit[0]] = unit[1]
                        secKey = header['Sec-WebSocket-Key']
                        resKey = base64.encodestring(hashlib.new("sha1",(secKey+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode('utf-8')).digest())
                        resKey = resKey.decode().replace("\n","")
                        response = '''HTTP/1.1 101 Switching Protocols\r\n'''
                        response += '''Upgrade: websocket\r\n'''
                        response += '''Connection: Upgrade\r\n'''
                        response += '''Sec-WebSocket-Accept: %s\r\n\r\n'''%(resKey,)
                        try:
                            self.con.send(bytes(response,'latin-1'))
                            self.isHandleShake = True
                            self.sendData("SETUID")
                            self.io.onConnect(self.uid)
                            time.sleep(1)
                        except:
                            return
                        continue

                except Exception as e:
                    self.socketThreadRunning = False
                    exc_type, ex, tb = sys.exc_info()
                    imported_tb_info = traceback.extract_tb(tb)[-1]
                    line_number = imported_tb_info[1]
                    print_format = '{}: Exception in line: {}, message: {}'
                    mirror.text(print_format.format(exc_type.__name__, line_number, ex))
                    mirror.text(traceback.format_exc())
                    continue

            else:
                try:
                    self.con.setblocking(0)
                    if "closed" in str(self.con):
                            return
                    ready = select.select([self.con], [], [], 1)

                    if ready[0]:
                        if "closed" in str(self.con):
                            return
                        data_head = self.con.recv(1).decode('latin-1')

                        if repr(data_head) == '':
                            self.onClose("1")
                            return

                        if "closed" in str(self.con):
                            return

                        try:
                            header = struct.unpack("B",bytes(data_head,'latin-1'))[0]
                        except:
                            return

                        opcode = header & 0b00001111

                        if opcode == 8:
                            if self.verbose == True:
                                mirror.text("* Closing Connection.")
                            self.socketThreadRunning = False
                            self.onClose("2")
                            continue

                        if "closed" in str(self.con):
                            return
                            
                        data_length = self.con.recv(1).decode('latin-1')
                        data_lengths= struct.unpack("B",bytes(data_length,'latin-1'))
                        data_length = data_lengths[0]& 0b01111111
                        masking = data_lengths[0] >> 7
                        
                        if data_length<=125:
                            payloadLength = data_length
                        elif data_length==126:
                            payloadLength = struct.unpack("H",bytes(self.con.recv(2).decode('latin-1'),'latin-1'))[0]
                        elif data_length==127:
                            payloadLength = struct.unpack("Q",bytes(self.con.recv(8).decode('latin-1'),'latin-1'))[0]
                        
                        if masking==1:
                            if "closed" in str(self.con):
                                return
                            maskingKey = self.con.recv(4).decode('latin-1')
                            self.maskingKey = maskingKey
                        data = self.con.recv(payloadLength).decode('latin-1')
                        if masking==1:
                            i = 0
                            true_data = ''
                            for d in data:
                                true_data += chr(ord(d) ^ ord(maskingKey[i%4]))
                                i += 1
                            self.onData(true_data)
                        else:
                            self.onData(data)

                except socket.error as e:
                    mirror.text(traceback.format_exc())
                    mirror.text("= E.12 Socket Error: " + str(e.errno))
                    if e.errno == 10035:
                        #self.time_delay += .001
                        #time.sleep(self.time_delay)
                        continue

                    if e.errno == 9 or e.errno == 10053 or e.errno == 10054 or e.errno == 10038:
                        self.socketThreadRunning = False
                        
                    self.socketThreadRunning = False
                    self.onClose("3")
                    return
            
            
    def onData(self,text) :
        try:
            uid,sign,value = text.split("<split>")
            uid = int(uid)
            if self.verbose == True:
                mirror.text("CLIENT >>> " + (value).replace(':::','.'))
        except:
            self.con.close()
        hashStr = hashlib.new("md5",(str(uid)+self.signKey).encode('utf-8')).hexdigest()
        if hashStr!=sign:
            mirror.text(" CyWebSocket.py onData() [ Browser Hash Invalid ]")
            self.con.close()
            return
        return self.io.onData(uid,value)

    def onClose(self, location):
        if self.verbose == True:
            mirror.text("* Closing from location: " + str(location))
        self.socketThreadRunning = False
        #self.io.setInfo("generic","False")
        
        if "closed" not in str(self.con):
            if eval(self.io.getInfo("noweb")) == False:
                self.con.close()
                self.io.onClose("CyWebSocket")
                return
        

    def packData(self,text):
        
        sign = hashlib.new("md5",(str(self.uid)+self.signKey).encode('utf-8')).hexdigest()
        data = '%s<split>%s<split>%s'%(self.uid,sign,text)
        return data
    
    def sendOVint(self, text):
        try:
            ov_split = str(text).split(",")
            
            if self.ov_packetCount >= self.ovsamples:
                if self.con == None:
                    return
                self.con.sendall(self.ovData) 
                self.ovData = bytes()
                self.ov_packetCount = 0
            
            ov_ints = list(map(lambda x: int(x), ov_split))
            self.ovData += b''.join((struct.pack('>h', val) for val in ov_ints))
            self.ov_packetCount += 1
            
        except Exception as e:
            self.socketThreadRunning = False
            self.onClose("3")
            return
            
    def sendOVfloat(self, text):
        try:          
            ov_split = str(text).split(",")
            
            if self.ov_packetCount >= self.ovsamples:
                if self.con == None:
                    return
                self.con.sendall(self.ovData)
                self.ovData = bytes()
                self.ov_packetCount = 0
            
            ov_floats = list(map(lambda x: float(x), ov_split))

            self.ovData += b''.join((struct.pack('>f', val) for val in ov_floats))
            self.ov_packetCount += 1
            
        except Exception as e:
            self.socketThreadRunning = False
            self.onClose("3")
            return
            
    def sendData(self, text):
        
        if eval(self.io.getInfo("status")) == False:
            return
            
        if eval(self.io.getInfo("noweb")) == True:
            if "outputdata" not in self.io.getInfo("config"):
                mirror.text(str(text))
            return "noweb"
        
        if self.uid == 0:
            try:
                text += "\r\n"
                text = bytes(text, 'utf-8')
                self.con.send(text)
                if self.verbose == True:
                    if len(text) > 50:
                        return
                    mirror.text("CLIENT <<< " + str(text))
            except Exception as e:
                self.socketThreadRunning = False
                self.io.setInfo("status","False")
                self.onClose("cyWebSocket sendData()")
                mirror.text(" ==== CyWebSocket().sendData() - (TEXT) Send Data Failure. ")

        else: 
            try:
                
                text = self.packData(text)
                if "closed" in str(self.con):
                    self.socketThreadRunning = False
                    self.io.setInfo("status","False")
                    return
                self.con.send(struct.pack("!B",0x81))
                length = len(text)

                if length<=125:
                    self.con.send(struct.pack("!B",length))

                elif length<=65536:
                    self.con.send(struct.pack("!B",126))
                    self.con.send(struct.pack("!H",length))
                else:
                    self.con.send(struct.pack("!B",127))
                    self.con.send(struct.pack("!Q",length))

                self.con.send(struct.pack("!%ds"%(length,),bytes(text, 'utf-8')))

            except Exception as e:
                if e.errno == 10038:
                    self.socketThreadRunning = False
                    return

                exc_type, ex, tb = sys.exc_info()
                imported_tb_info = traceback.extract_tb(tb)[-1]
                line_number = imported_tb_info[1]
                print_format = '{}: Exception in line: {}, message: {}'
                mirror.text(" ==== CyWebSocket().sendData() - (WEB CLIENT) Send Data Failure. ")
                mirror.text(" =E4. " + print_format.format(exc_type.__name__, line_number, ex))
                mirror.text(traceback.format_exc())
                return
