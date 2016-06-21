CyKit FAQ
==========

Battery Questions
=================

* What is my average battery lifetime?<br>
   developer edition is about 12 hours.<br>
   insight edition is about 4 hours.<br>
   scientific edition is about 12 hours in dev mode,<br>
   6 hours in scientific mode, which uses bluetooth LE which uses less energy<br>
   however sends a higher resolution of data that costs more energy.<br>

* What is the amount of charge the battery can hold?<br>
   680 milliamps per hour.

* Could this device shock me?<br>
   You can not get shocked from the sensor contact as there is no electricity<br>
   (from the headset) going through the contact wires. The battery and microchip<br>
   is self-contained. However if they somehow did get wet, it is possible, but <br>
   its more likely it would short out the connections first and many key points<br>
   would have to be covered in water. I strongly advise against submerging this in water.<br>


* What measurement of voltage from the mind am I getting back from the data?<br>
    The (LSB)least-significant-bit (1st binary digit, ie the far right place of a binary number)<br>
    of a fourteen-bit value is equivelant to 0.13 to 0.51µV<br>
    
    developer headset is equivelant to 0.51µV (microvolts).<br>
    scientific headset & insight models are equivelant to 0.13µV (microvolts).


Sensor Questions
================
* Can I remove the felt pads in the contact sensors?<br>
   Yes.

* How do I remove the sensor contact?<br>
   Turn the black contact a quarter-turn, do not over-tighten! (Known to break)

* What are the sensor contacts made out of?<br>
   gold coated with a polymer.

* Is the (green)Oxidation of the Contacts normal?<br>
   Yes. The polymer is just a host for an electrochemically<br>
   active material which reacts with the salt water. This is normal.

* What maintenance can i perform on my sensors? 

  Quantity of 0.4% to 0.9% saline.<br>
  Small quantity (50 mil) pure isopropyl alcohol.<br>
 Six good quality cotton (ear) buds.<br>

   Following the instructions provided by Emotiv systems, remove all of the contacts from the headset arms (or fingers). Remove the
   felt pads and soak them in a flat dish with about 2 mm of saline on the bottom. While the felt pads are soaking, wet a cotton bud
   with the alcohol and rub the gold contact in the felt pad holder. If there is a buildup of salts, let it soak a while and try
   again later. If necessary, flush out any debris from the salts using either alcohol or saline. IMPORTANT: Never use any type of
   sharp item to scrape the salts off. Even the smallest scratch will damage the contact and the underlying metal will be destroyed
   in time by the electrolysys process. Once all the gold contacts have been cleaned, you should now revive the felt pads. I have
   noticed (in the dry Australian summer) that the salts build up within the internal felt structure as vertical columns. You can
   often detect this by squeezing the pad sideways and then comparing that to squeezing it vertically. If it appears brittle or is
   noticeably stiffer when you compress it vertically, this is a good indication there is a columnar buildup. If needed, fully
   saturate the pad in saline for ten minutes then carefully squeeze it vertically to half its height then reshape it round again.
   If you flatten it too much, the pad may break apart. Repeat this a few times for each pad. You should notice a significant
   increase in comfort when you next use the headset. One at a time, shake off the excess saline from the pad and re-insert it into
   its holder. Screw the holder and pad assembly into the socket on the headset arm. At all times, you should avoid letting any
   liquid get into the electronics. Connect   everything up again and test the headset with the Emotiv Control Panel. 
   
   DISCLAIMER:
   While the above process has worked very well for me, it is your responsibility to enure it is suitable for your needs.
   
   
* Do the sensor wires contain voltage?<br>
   No. The battery operates the detection electronics, 
   signal processing microprocessor and the wireless transmitter.

* Is it possible to damage my gold sensor contact?<br>
   Yes! Do not clean the contact plate with anything. There is a polymer layer there which contains the materials required for
   low-noise electrolytic contact. A bit of green on it does no harm at all. 

Headset Questions
=================

* What is the headset made out of?<br>
   polypropylene

* What is the headset arms made of?<br>
   polycarbonate


Wireless Questions
========================
* What frequency does the epoc headset operate at?<br>
   2.4ghz, same as a cordless phone or wireless device.<br>
   epoc+ and Insight utilizes bluetooth 4.0 LE. (Low Energy standard)
   
* How is my data encrypted?
   The encryption is rjindael which is a form of AES encryption.
   emotiv.py imports this.



* Why is there 16 contacts?<br>
   There are 14 voltage sensor points on EPOC, measuring voltages relative to one of the two reference points. The other
   reference point is used to cancel background noise, which is why there are 16 sensors. 

General Questions
=================

* Do I need an arduino controller (i.e. Raspberry Pi)?<br>
   No. Plug in Emotiv USB dongle and it should connect.

* Why did you change the emoKit name to CyKit?<br>
   I've been wanting to change it for a long time and I thought
   CyKit sounded cool. I take absolutely no credit in creating the core 
   emoKit files (Except for the socket streaming.) I also mean no
   disrespect to the authors by changing the name and would like to 
   thank them for their hard work.

* What model of epoc should I get?<br>
   
   Insight model - is designed for the casual consumer on the go, its bluetooth capable and
   can connect with other wireless devices, as well can make use of the "extention
   accessory" which is able to record to an SSD.  another feature is its "Long Life
   Semi-dry Polymer" contact sensor, which does not require saline as its a type of
   sealed wet gelpak.  This device can send twice the data (sample rate), however its
   limitation is that it only has 5 sensors.

   EPOC+ or the Scientific model - is the same as the EPOC model with some improvements.
   It has 4x the resolution than the EPOC picking up 0.14 microvolts.  
   Bluetooth capable, it also features a 9 axis sensor (3x gyro, 3x accelerometer, 3x magnetometer)
   Could find some use in virtual Reality entertainment perhaps, or users with low mobility
   Also the ability for wired USB, with an "extention" accessory". Like the insight
   it also features double the sample rate, 256 samples, opposed to EPOCs 128 samples.
   It has ability to disable some of its channels as well for extended power life.
   
   Developer model - If you have a budget in mind, may be your best option.
   it has 14 sensors and covers 3x more surface area of the brain than the insight,
   but at half the sample rate.  I believe its an all around good choice. I do have
   some issues with its durability. If you really need one. I recommend the developer
   model, and might even spring for an EPOC+. If you can hold off, I'd wait until they
   come out with a new model, maybe one that has a more solid headset, makes use of the
   long life contacts and the improved sample rates. 

* What is the "extention accessory" ?<br>
   This is an accessory that can record to an SD card
   hooks up directly to the EPOC+ and Insight models.
   Can hook up a "extention hardware trigger"

* What is an "extention hardware trigger" ?<br>
   This is more or less a wired remote that has a button/trigger you press,
   when its pressed, it communicates with the EEG software, (most likely testbench).
   It then places 'markers' indicating exactly when the trigger was pressed, this
   can be useful in determining interaction with the environment and the corrolating
   brain activity that followed.
   

Data Questions
==============

* What data does Cykit give me?<br>
    Same functionality as emoKit.<br>
    Streams the raw data from the channels of the headset<br>

* What data does Cykit not give me?<br>
   Processed data, i.e data that has been sifted through identifying<br>
   key patterns related to facial expressions and muscle movements.

* How do I read the data from the emotiv script?
   Try an example script, or render.py
   you first dequeue the buffer, this places all the packet into your
   packet variable. You also specify which sensor you want to read from
   that packet variable.

* What format and range of data am I getting back? 
   Emokit parses the sensor values as an unsigned integer.
   Thus, to get values between -8192 and 8192, subtract 8192. 

* How does the scientific model have a better resolution than the developer?
   EPOC+ advantages are: option for higher voltage resolution (4x better, 0.14 vs 0.51uV)
   option for higher sample rate (256 vs 128 per sec), compatibility with more mobile 
   devices via low energy Bluetooth® Smart (high res modes not available over BT) 
   and better motion sensor 9 axis vs 2 axis gyro). 
 
* What measurement of voltage from the mind am I getting back from the data?<br>
    The least-significant-bit(LSB)(ie the far right place of a binary digit)
    of the fourteen-bit value<br>
    developer headset is equivelant to 0.51µV (microvolts).
    the scientific headset & insight models is equivelant to 0.31µV (microvolts).

Programming Questions
=====================
 
 * What are the sensor bytes for the packet buffer? <br>
    F3 FC5 AF3 F7 T7 P7 O1 O2 P8 T8 F8 AF4 FC6 F4
    example packet.AF3

Python 3 Support
===================

https://github.com/CymatiCorp/CyKit-Python-3.3

Is a Windows Port for Python 3.3

the changes to emotiv.py and dependancies are a simple fix of changing
print function syntax and Exception syntax. 

gevent / greenlet, has now been updated to support Python 3

The most difficult part of porting to Python 3, is that Python 3 is
stricter about string formatting and defining the UTF setup.

There is really no benefit or improvement that I can tell to moving to
Python 3, other than having the most current up to date software.
With no real speed improvements, the only reason that it might be beneficial
is if you might want to make take advantage of newer gevent/greenlet functions.
