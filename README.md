
<img src="http://cymaticorp.com/edu/cykit4.png" width=25% height=25% ><br>
CyKit 1.0 for Python 2.7.6 (Windows x86) using Emotiv EPOC headset.<br><br>
FAQ<br>
https://github.com/CymatiCorp/CyKit/blob/master/FAQ.md <br>

Wiki (Updated Jan. 2015)<br>
https://github.com/CymatiCorp/CyKit/wiki/EEG-CyKit-1.0-updates <br>

<img src='http://cymaticorp.com/edu/dash/particle.png' width=10% height=10%></img>
<img src='http://cymaticorp.com/edu/dash/particle2.png' width=10% height=10%></img>
<img src='http://cymaticorp.com/edu/dash/particle3.png' width=10% height=10%></img>
<img src='http://cymaticorp.com/edu/dash/particle32.png' width=10% height=10%></img>
<br><br>

OpenVIBE Setup (Updated Feb 25 2015) <br>
https://github.com/CymatiCorp/CyKit/blob/master/Openvibe-Readme.md

<img src='http://cymaticorp.com/edu/matrix.png' width=50% height=50%></img><br>

Cyos (OpenViBE TCP Server - Revision 1.0 - Win32 Executable)<br>
http://cymaticorp.com/edu/github/Cyos-0.1.0.win32.py2.7.zip <br>

Hardware<br>
https://github.com/CymatiCorp/CyKit/blob/master/Hardware-Readme.md <br>
<img src = http://cymaticorp.com/edu/IMG_0004.JPG width=10% height=10% />
<img src = http://cymaticorp.com/edu/IMG_0015.JPG width=10% height=10% />

Modified Hardware<br>
<img src = http://cymaticorp.com/edu/cy1.png width=10% height=10% />
<img src = http://cymaticorp.com/edu/cy2.png width=10% height=10% />
<img src = http://cymaticorp.com/edu/cy3.png width=10% height=10% />


Questions about the project?<br>
Contact me at warrenarea@gmail.com

Description
-----------
CyKit 1.0 is specifically for Python development in Windows to<br>
give access to the raw data stream from the Emotiv EPOC headset.  <br>
CyKit 1.0 is an unofficial branch to the OpenYou emoKit, check it out here<br>
 https://github.com/openyou/emokit <br><br>
<img src='http://cymaticorp.com/edu/render11.png' width=27% height=21%></img>


CyKit Dependencies
--------------------
* pywinusb 0.2.9
* pycrypto 2.6
* gevent 1.0.1
* greenlet 0.4.2 (or Newest 0.4.5)
* pygame 1.9.1 (Only required if you want to use render.py
   which shows the EEG graph)

Python Usage
------------
  Code:
  
    import emotiv
    import gevent

    if __name__ == "__main__":
      headset = emotiv.Emotiv()    
      gevent.spawn(headset.setup)
      gevent.sleep(1)
      try:
        while True:
          packet = headset.dequeue()
          # packet.byteCode --- See Byte Codes below. 
          print packet.gyroX, packet.gyroY
          gevent.sleep(0)
      except KeyboardInterrupt:
        headset.close()
      finally:
        headset.close()


Direct links for Windows(x86) Dependencies
------------------------------------------
* pywinusb - https://pypi.python.org/packages/source/p/pywinusb/pywinusb-0.2.9.zip
* pycrypto - http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe
* gevent   - www.lfd.uci.edu/~gohlke/pythonlibs/#gevent ->  gevent‑1.0.1.win32‑py2.7.exe
* greenlet -  https://pypi.python.org/packages/2.7/g/greenlet/greenlet-0.4.2.win32-py2.7.exe#md5=0ea8f5a14f8554919e1a136bc042d76c
* Pygame(optional) - http://pygame.org/ftp/pygame-1.9.1.win32-py2.7.msi

Note: Python 3.4.2 is not supported as gevent has not been updated to support it.<br>
       please see the FAQ [here](https://github.com/CymatiCorp/CyKit/blob/master/FAQ.md#Python) for more information.
       

Installation Instructions (Using Windows binaries)
--------------------------------------------------
* Install Python 2.7.6 https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi


Extract pywinusb to any folder,  and copy the folder

                                       \pywinusb 
                                       
                                  from folder \pywinusb-0.2.9 to
                                        
                                 Drive:\Python27\Lib\site-packages
                                       
* Install following dependancies:

 gevent 1.0.1

 greenlet 0.4.2
 
 pycrypto 2.6
 
  
  Install to python2.7.6 folder.

Navigate to the Python directory extracted from CyKit-master.zip

C:\Python27\Python.exe C:\Cy-master\Python\example.py

If your Emotiv USB dongle is not connected it will throw several errors ending with:



                                       AttributeError: 'Emotiv' object has no attribute 'device'


Connect the EPOC USB dongle and run again, and it should begin streaming you data.


   
Alternate Installation (Using the PIP package installer)
--------------------------------------------------------

* Install Python 2.7.6 https://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
 
Extract pywinusb to any folder,  and copy the folder

                                       \pywinusb 
                                       
                                  from folder \pywinusb-0.2.9 to
                                        
                                 Drive:\Python27\Lib\site-packages
                                       
 
 Install pycrypto 2.6
 
 Download PIP from its website:  https://bootstrap.pypa.io/get-pip.py <br>
  (Place get-pip.py in your Python folder.)

Run:

                         python.exe get-pip.py
                         python.exe -m pip install greenlet
                         python.exe -m easy_install greenlet
                         python.exe -m pip install gevent

PIP downloads the latest versions of these projects.
 Current versions:
 
                       greenlet 0.4.5
                       gevent 1.0.1




Byte Codes
----------
This is a list of the byte names you can receive through packet.
( For example print packet.AF4 )

  F3  FC5  AF3  F7  T7  P7  O1  O2  P8  T8  F8  AF4  FC6  F4

Server Support
==============
Added ability to stream the data to a TCP connection. <br>
Adjust Python PATH in batch files as necessary.
Type RunStream.bat

    runs: Python.exe stream.py <server> <port>


mIRC Support
=============
<img src='http://cymaticorp.com/edu/emotKit1.png' width=40% height=40%></img> 

Added a mIRC script that will connect to the TCP server and display
in a simple graph the activity of the sensors. 

In Command Prompt type RunStream.bat

     (runs: Python.exe stream.py <ip> <port> )

In mIRC "Status Window" type 

     /load -rs CyClient.mrc
     /load -rs CySignal.mrc

This loads scripts to the remotes. Alternatives ALT+R and load manually.
then in "Status Window" type. 

CyClient.mrc - Connects to the socket server and breaks large packets into smaller ones.
CySignal.mrc - Receives the smaller packets and handles displaying EEG results.

     /EEG
       or Popup Menu: EEG
       

<img src='http://cymaticorp.com/edu/cykit-mirc-1.png' width=40% height=40%></img>

Updated mIRC so that it averages out the data, creating baselines for each data 
channel.  This means, no matter what signal variance or whether the data has a 
positive or negative sign, the data displayed can then be placed equally from
one another on seperate lines. Setting a baseline only needs to occur once per
EEG run. It will do it automatically when your device is connected to the stream, 
but you can optionally initiate a baseline reset manually in your status pop-up window.



Credits & Original Code
=======================

* Cody Brocious (http://github.com/daeken)
* Kyle Machulis (http://github.com/qdot)

Contributions by

* Severin Lemaignan - Base C Library and mcrypt functionality
* Sharif Olorin  (https://github.com/fractalcat) - hidapi support and project guru
* Bill Schumacher (https://github.com/bschumacher) - Fixed the Python library (again)
* Bryan Bishop and others in #hplusroadmap on Freenode.
* Warren - (https://github.com/CymatiCorp/CyKit) Socket server.

