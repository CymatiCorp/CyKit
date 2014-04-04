Emotkit 1.0
===========

Description
===========

Emokit is a set of language for user space access to the raw stream
data from the Emotiv EPOC headset. Note that this will not give you
processed data (i.e. anything available in the Emo Suites in the
software), just the raw sensor data.

The C library is backed by hidapi, and should work on any platform
that hidapi also works on.

Information
===========

FAQ (READ BEFORE FILING ISSUES): https://github.com/openyou/emokit/blob/master/FAQ.md

If you have a problem not covered in the FAQ, file it as an
issue on the github project.

PLEASE DO NOT EMAIL OR OTHERWISE CONTACT THE DEVELOPERS DIRECTLY.
Seriously. I'm sick of email and random facebook friendings asking for
help. What happens on the project stays on the project.

Issues: http://github.com/openyou/emokit/issues

If you are using the Python library and a research headset you may have to change the type in emotiv.py's setupCrypto function. 



Required Libraries
==================

Python
------

* pywinhid  - https://pypi.python.org/pypi/pywinusb/
* pyusb (OS X, Optional for Linux) - http://sourceforge.net/projects/pyusb/
* pycrypto - https://www.dlitz.net/software/pycrypto/
* gevent - http://gevent.org
* realpath - http://?   sudo apt-get install realpath

Python library
--------------

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
