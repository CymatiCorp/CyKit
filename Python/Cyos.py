#
#   Cykit OpenViBE Server
#
#    For use with "Generic RAW Telnet Stream" in OpenViBE Acquisition Server.
#     14 channels of Signed 16-bit BIG-Endian Integers in non-delimited byte string.
#     2 Bytes per Channel.
#     with no CRLF terminating characters.
#

import socket
import gevent
import sys
import struct

sys.path.insert(1, './Python/CyKit/')
import emotiv
if len(sys.argv) < 3 or len(sys.argv) < 2:
   print "Usage:  Python.exe stream.py IP Port"
   sys.argv = [sys.argv[0], "localhost", "5555"]
   print "Defaulting to localhost:5555"


def main():

    try:         
         connectServer()
                  
    except Exception, e:
         print(e)

    gevent.sleep(0.1)
    try:
       while True: 
            
             packet = headset.dequeue()
             cy = ""
             values = [packet.sensors[name]['value'] for name in 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' ')]
             cy = struct.pack('>' + str(len(values)) + 'h',*values)
             conn.sendall(cy)

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
