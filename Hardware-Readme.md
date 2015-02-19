<img src= http://blueskynet.org/edu/emotiv.jpg width=25% height=25% />

Hardware Update January 2015
============================

Reassembled my latest epoc headset.  The plastic was breaking down with minimal use<br>
   so I redesigned it.  I cut out a piece of cardboard about the size of my palm and<br>
   poked holes in the desired contact points. Then glued a layer of aluminum foil over<br>
   that. Next I cut out a piece of foam and glued that to the cardboard, poking holes<br>
   in the foam.  Then threaded the wires through and glued the contact casings in place<br>
   inset in the foam.  After all contacts were in place, I put a thin layer of glue<br>
   over the foam. This is for when I spray down the contacts, that the foam doesn't get<br>
   saturated. I mounted the battery and the control boards on the back of the unit. <br>
   next i attached an elastic headband to the sides of the unit, so when I place it on<br>
   my head, it is quite snug and there is less worry about the slightest movement<br>
   skewing any results. The device appears to work, however I think the contacts are<br>
   a bit too close together for my liking. <br><br>
   over all, i'm happy with my design, except I'd prefer to have spread out the contact.s<br>
   I tested the signal quality in epoc control panel today and it<br>
   was green across the board. Still have some quandary's of what impact the<br>
   locations of the reference sensors are playing, and whether the proximity is<br>
   an issue.<br><br>
   
Modifying your Headset
======================
if you do decide to modify your unitt, please follow these instructions.<br>
it will save you a lot of grief.

   1. Take pictures of wiring asap.
   2. carefully saw the plastic, do not pry.
   3. as soon as you get to a bundle of wiring.<br>
      tape them together in a bundle.<br>
   4. as soon as you get to the control boards. refer to step 1. <br>
      and hot glue the contact points of "all" the wires in their place.<br>
      these wires are very brittle and is the reason for step 2.   <br>
   5. cut the battery wires one at a time, tape the ends off of the battery<br>
      and put away from your work area. <br>
   6. according to emotiv forums it is counter-intuitive to put sensors<br>
      too close in a cluster as its picking up groups of neurons firing at once.<br>
   7. elastic headband approach works well. plus can give you alternate sites<br>
      for testing.<br>
   8. the black wires are reference point wires and are crucial to the device <br>
      working properly.  you only need only 2 sensor nodes. (though there are 4 contact slots) <br>
      you can always wire the 2 extra contact wires to the 2 reference points you are using.<br>

   
The pictures below are images from my "old" epoc headset that is no longer
with us. lets just say it didnt make it past step 5.

Wiring Layout
=============

Top Sensor Circuit, to Power Driver Circuit.

* Black (Ground)
* Red (Battery)
* Blue
* Green
* Brown
* Yellow (Gyro)
* Gray (Gyro)

Bottom board of Sensor Circuit, To Sensor Contacts.<br>
(Same color coding for both sides)

* Brown
* Green
* Red
* Black (2 wires) - Reference contacts to measure impedance.
* Gray
* Orange
* Blue
* Yellow

Driver (Power) Circuit, to Top Sensor Circuit.

* Gray (Gyro)
* Yellow (Gyro)
* Brown
* Green
* Blue
* Red  (Battery)
* Black (Ground)

Note: The solder point for the black wire has two wires attached to it,
 as this is the 2 reference contacts that can be alternated. Reference
 points do not measure EEG data, but rather the impedance of the surface
 area its measuring. This is involved in measuring signal quality.<br><br>
 The images are missing a couple of wires, so this should show you the
 exact color code ordering.

The Hardware
============

Sensor Chip for headset (Front)<br><br>
<img src = http://blueskynet.org/edu/IMG_0004.JPG width=25% height=25% />

Contacts and Wiring<br><br>
<img src = http://blueskynet.org/edu/IMG_0015.JPG width=25% height=25% />

Sensor Chip for Headset (Back)<br><br>
<img src = http://blueskynet.org/edu/IMG_0017.JPG width=25% height=25% />

Sensor Chip for Headset (Front)<br><br>
<img src = http://blueskynet.org/edu/IMG_0018.JPG width=25% height=25% />

Sensor Contact (Gold plated silver)<br><br>
<img src = http://blueskynet.org/edu/IMG_0028.JPG width=25% height=25% />

Driver for Sensor Chip. Battery Charging and Delivery.<br>
Red LED to indicate Charging, Blue LED to indicate turned on.<br><br>
<img src = http://blueskynet.org/edu/IMG_0031.JPG width=25% height=25% />

Epoc Headset Frame<br><br>
<img src = http://blueskynet.org/edu/headset.JPG width=25% height=25% />
<br><br>

Modified Epoc Headset Frame (1st)
===================================
(Retired)<br><br>

<img src = http://blueskynet.org/edu/headset2.JPG width=25% height=25% />
<br><br>
<img src = http://blueskynet.org/edu/i2.JPG width=25% height=25% />
<br><br>

Modified Epoc Headset Frame (2nd)
===================================
(Active)<br><br>

<img src = http://blueskynet.org/edu/cy1.png width=25% height=25% />
<br><br>
<img src = http://blueskynet.org/edu/cy2.png width=25% height=25% />
<br><br>
<img src = http://blueskynet.org/edu/cy3.png width=25% height=25% />
<br><br>
