CyKit FAQ
==========


Sensor Questions
================
* Can I remove the felt pads in the contact sensors?<br>
   Yes.

* How do I remove the sensor contact?<br>
   Turn the black contact a quarter-turn, do not over-tighten!

* What are the sensor contacts made out of?<br>
   gold coated with a polymer.

* Is the (green)Oxidation of the Contacts normal?<br>
   Yes. The polymer is just a host for elecrochemically active material<br>
   which reacts with the salt water. This is normal.

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
   itâ€™s holder. Screw the holder and pad assembly into the socket on the headset arm. At all times, you should avoid letting any
   liquid get into the electronics. Connect   everything up again and test the headset with the Emotiv Control Panel. DISCLAIMER:
   While the above process has worked very well for me, it is your responsibility to enure it is suitable for your needs.
   
   
* Do the sensor wires contain voltage?<br>
   No. The battery operates the detection electronics, 
   signal processing microprocessor and the wireless transmitter.

* Is it possible to damage my gold sensor contact?<br>
   Yes! Do not clean the contact plate with anything. There is a polymer layer there which contains the materials required for
   low-noise electrolytic contact. A bit of green on it does no harm at all. 

* What is the headset made out of?<br>
   polypropylene

* What is the headset arms made of?<br>
   polycarbonate

* What frequency does the epoc headset operate at?<br>
   2.4ghz, same as a cordless phone or wireless device.<br>
   epoc+ and Insight utilizes bluetooth 4.0 LE. (Low Energy standard)
   

* Why is there 16 contacts?<br>
   There are 14 voltage sensor points on EPOC, measuring voltages relative to one of the two reference points. The other reference
   point is used to cancel background noise, which is why there are 16 sensors. 

* What data does Cykit give me?<br>
    Same functionality as emoKit.<br>
    Streams the raw data from the channels of the headset<br>

* What data does Cykit not give me?<br>
   Processed data, i.e data that has been sifted through identifying<br>
   key patterns related to facial expressions and muscle movements.

* Do I need an arduino controller (i.e. Raspberry Pi)?<br>
   No. Plug in Emotiv USB dongle and it should connect.

* Why did you change the emoKit name to CyKit?<br>
   I've been wanting to change it for a long time and I thought
   CyKit sounded cool. I take absolutely no credit in creating the core 
   emoKit files (Except for the socket streaming.) I also mean no
   disrespect to the authors by changing the name and would like to 
   thank them for their hard work.

* What measurement of voltage from the mind am I getting back from the data?<br>
    The least-significant-bit(LSB)(ie the far right place of a binary digit)
    of the fourteen-bit value<br>
    developer headset is equivelant to 0.51µV (microvolts).
    the scientific headset & insight models is equivelant to 0.31µV (microvolts).

* What is my average battery lifetime?
   developer edition is about 12 hours.
   insight edition is about 4 hours.
   scientific edition is about 12 hours in dev mode,<br>
   6 hours in scientific mode, which uses bluetooth LE
   but sends a higher resolution of data.

* What model of epoc should I get? 
   It depends on your needs,  the Insight model is more of a commercial version and
   may be more equiped for casual users, also I believe its design to be more mobile
   and suited for the outdoors.  Although its collection of data is very limited with
   only 5 sensors.  It also has superior sensors not available in other models,  they
   use a "Long life semi-dry polymer"  that contains liquid in them, but it reportedly
   lasts for a very long time. This means no watering your contacts with saline or
   trying to fiddle with your contacts in general.

   The scientific model, called epoc+ is the same as the epoc model, with a few minor
   differences. one being slightly better resolution, bluetooth which may be good for
   security reasons.  It also features a 9 axis sensor (3x gyro, 3x accelerometer, 3x magnetometer)
   which I'm sure there may be some uses for that, particularly in the area of virtual
   reality entertainment perhaps. For me, this is not a feature I can not live without.
   One positive for epoc+ is the ability for wired USB, with an "extention" accessory.
   This accessory also has a "extender hardware trigger", where you press a button and
   you are able to mark the exact point in the EEG where you pressed the button, this
   can be useful for corrolating EEG with the environment.  Also with the extention 
   accessory is the ability to record to an SD card, this could be useful for mobility,
   or just sake of format. 
   
   the developer model is pretty straight forward, and if you have a budget in mind, may
   be your best option. it has 14 sensors and covers 3x more surface area of the brain
   than the insight. I believe its an all around good choice, but I have seen lots of
   reports and experienced first-hand the headset plastic breaking from casual use. Not
   to say any other model (than perhaps the insight) will offer.  If you really want a
   headset, I recommend the developer model, but long-term it may be more prudent to
   wait for the next model. Perhaps they can solve their materials issue and will have
   support the new semi-dry polymer contacts with all the other great features (if not
   a new headset design entirely). Though You can be sure the next model will be 
   equally expensive as the insight or the scientific model.
   
