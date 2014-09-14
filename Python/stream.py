from EmotKit import emotiv
import gevent
import socket

def main():
    headset = emotiv.Emotiv()
    gevent.spawn(headset.setup)
    connectServer()
    gevent.sleep(1)
    try:
       while True: 
             packet = headset.dequeue()
             connbuffer = ""

             for name in 'AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4'.split(' '):
              connbuffer += " " +  str(packet.sensors[name]['value']) 
             conn.send(connbuffer)
            #conn.sendall(connbuffer + b'\0')  
            #This sends 14 sensors on one terminating line but packet data is skipped.
             connbuffer = ""
    except KeyboardInterrupt:
             conn.close()
             headset.close()
    finally:
             conn.close()
             headset.close()

def connectServer():
     global conn
     HOST = 'localhost'
     PORT = 21013
     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     s.bind((HOST, PORT))
     s.listen(1)
     conn, addr = s.accept()
     print 'Connected to', addr


try:
  print "Connect to 127.0.0.1 : 21013"
  main()
  
except Exception, e:
  print e
  print "Device Time Out or Disconnect . . . Reconnect to Server."
  conn.close()
  main()
