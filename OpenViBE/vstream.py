import socket
import gevent
import sys
import numpy as np
import struct
import binascii

sys.path.insert(1, './Python/CyKit/')
import emotiv
if len(sys.argv) < 3 or len(sys.argv) < 2:
   print "Usage:  Python.exe stream.py IP Port"
   sys.argv = [sys.argv[0], "localhost", "55555"]
   print "Defaulting to localhost:55555"

 
def main():

    try:         
         

         connectServer()
                  
    except Exception, e:
         print(e)

    gevent.sleep(0.05)
    try:
       while True: 
             packet = headset.dequeue()
             connbuffer = ""
             cbs = ""
             x = np.array([ cval(packet.sensors['AF3']['value']),
                                 cval(packet.sensors['F7']['value']),
                                 cval(packet.sensors['F3']['value']),
                                 cval(packet.sensors['FC5']['value']),
                                 cval(packet.sensors['T7']['value']),
                                 cval(packet.sensors['P7']['value']),
                                 cval(packet.sensors['O1']['value']),
                                 cval(packet.sensors['O2']['value']),
                                 cval(packet.sensors['P8']['value']),
                                 cval(packet.sensors['T8']['value']),
                                 cval(packet.sensors['FC6']['value']),
                                 cval(packet.sensors['F4']['value']),
                                 cval(packet.sensors['F8']['value']),
                                 cval(packet.sensors['AF4']['value']) ], dtype = ">u4")
              
             y = x.byteswap()
             connbuffer = str(y.data)
             cbs = connbuffer
             cbs = connbuffer.replace('\x00', '')
             cbs = '\x20\x20\x20\x20' + cbs
             conn.sendall(cbs + '\r\n')
             
    except Exception as msg:
             print 'Error: ' + str(msg)
             conn.close()

    finally:
             print "Disconnecting . . ."
             conn.close()
             gevent.GreenletExit
             print "Restarting . . ."
             main()

def cval(cv):
     return abs(cv)


def connectServer():
     global conn
     HOST = str(sys.argv[1])
     PORT = int(sys.argv[2])
     print "Listening to " + HOST + " : " + str(PORT)
     try:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     except socket.error as msg:
         s = None

     try:
         s.bind((HOST, PORT))
         s.listen(1)
     except socket.error as msg:
         s.close()
         s = None

     if s is None:
         print 'Could not open socket'
         return
     
     conn, addr = s.accept()
     print 'Listening to', addr
     

try:
  headset = emotiv.Emotiv(True, False)
  gevent.spawn(headset.setup)
  main()

except Exception, e:
  print e
  print "Device Time Out or Disconnect . . .    Reconnect to Server."
  conn.close()
  main()
