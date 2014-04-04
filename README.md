EmotKit 1.0 for Python 2.7.6 in Windows
=======================================

Description
===========

EmotKit 1.0 is specifically for Python development in Windows to 
give access to the raw data stream from the Emotiv EPOC headset.  

Note that this will not give you processed data. 


EmotKit Dependancies
--------------------

* pywinusb
* pycrypto
* gevent 
* greenlet

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
          print packet.gyroX, packet.gyroY
          gevent.sleep(0)
      except KeyboardInterrupt:
        headset.close()
      finally:
        headset.close()


Direct links for Windows(x86) Dependancies
------------------------------------------

* pywinusb - https://pypi.python.org/packages/source/p/pywinusb/pywinusb-0.2.9.zip
* pycrypto - http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe
* gevent   - http://www.lfd.uci.edu/~gohlke/pythonlibs/sn5ub7d9/gevent-1.0.win32-py2.7.exe
* greenlet -  https://pypi.python.org/packages/2.7/g/greenlet/greenlet-0.4.2.win32-py2.7.exe#md5=0ea8f5a14f8554919e1a136bc042d76c


Installation Instructions
-------------------------

* Install Python 2.6.7

Extract pywinusb to any folder,  and copy 

                                       \pywinusb 
                                       
                                  from \pywinusb-0.2.9 to
                                        
                                 Drive:\Python27\Lib\site-packages
                                       
* Install following dependancies:
 gevent
 greenlet
 pycrypto 
 
  Install to python2.7.6

Navigate to the Python directory extracted from emotkit10.zip

C:\Python27\Python.exe C:\emotkit10\Python\example.py

If your Emotiv USB dongle is not connected it will throw several errors ending with:



                                       AttributeError: 'Emotiv' object has no attribute 'device'


Connect the Emotiv dongle and run again, and it should begin streaming you data.

Note: Python 3 requires some cosmetic updates to work properly. 
   

Notes 
-----
If you are using the Python library and a research headset you may
have to change the type in emotiv.py's setupCrypto function. 

Raspberry Pi is not required, just plug dongle into USB.


Credits & Original Code
=======================

* Cody Brocious (http://github.com/daeken)
* Kyle Machulis (http://github.com/qdot)

Contributions by

* Severin Lemaignan - Base C Library and mcrypt functionality
* Sharif Olorin  (http://github.com/fractalcat) - hidapi support
* Bill Schumacher (http://github.com/bschumacher) - Fixed the Python library
* Bryan Bishop and others in #hplusroadmap on Freenode.


