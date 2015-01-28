OpenViBE 0.14.0 
===============


<img src='http://blueskynet.org/edu/openvibe/acqure1.png' width=100% height=100%></img>
Figure A.

1. Select the "Generic Raw Telnet Reader" driver.
2. Set the 'Connection port' to the port you want OpenVibe to use. (ie 4444)
3. Set Sample block to 4 (mine only sends 1 sample and the picture says 16 samples)
4. Click "Driver Properties"
5. Number of Channels = 14
6. Sampling frequency = 128
7. Telnet hostname = localhost
8. Sample type = 16 bits unsigned integer
9. Apply.

<img src='http://blueskynet.org/edu/openvibe/acquire2.png' width=100% height=100%></img>
Figure B.

1. Navigate to your CyKit\RunStream.bat file and set your own custom port. (IE 21555)
2. Verify and Save.

<img src='http://blueskynet.org/edu/openvibe/acquire3.png' width=100% height=100%></img>
Figure C.

1. RunRender.bat<br>
   it should now say its connecting (or listening in this case.)
2. Click "Connect" on the OpenVIBE Acquisition server.


<img src='http://blueskynet.org/edu/openvibe/acquire4.png' width=100% height=100%></img>
Figure D.

1. Verify the Log will say "Connection succeeded!"
2. Verify Data is being read from the Python stream.py server.

<img src='http://blueskynet.org/edu/openvibe/acquire5.png' width=100% height=100%></img>
Figure E.

1. Run "OpenVIBE Designer"
2. Drag and drop "Acquisition Client" from Boxes (on the right) to the white window space on the left.
3. Drag and drop "Signal display" as well.
4. Hover over the pink arrow. "Signal Stream [signal]" drag a line from that arrow<br>
   to the green arrow "Signal [streamed matrix]" until a line connects them.
5. Double click "Acquisition Client"
6. Replace server hostname with "localhost"
7. Replace server port with your designated OpenVIBE port. (IE 4444)
8. Apply.

<img src='http://blueskynet.org/edu/openvibe/acquire55.png' width=100% height=100%></img>
Figure F.

1. Return to the "OpenVIBE acquisition server" and press "Play"

<img src='http://blueskynet.org/edu/openvibe/acquire6.png' width=100% height=100%></img>
Figure G.

1. Return to the "OpenVIBE Designer" and press "Play"

<img src='http://blueskynet.org/edu/openvibe/acquire7.png' width=40% height=40%></img>

Figure H.

1. A window will appear with your EEG stream.
2. Press Stop when completed or making signal changes.

<img src='http://blueskynet.org/edu/openvibe/acquire8.png' width=100% height=100%></img>

Figure I.

Additionally, to smooth out your EEG data.

1. Select the line between "Acquisition client" and press delete.
  (or right click and delete.)
2. Find "Signal Processing > Averaging > Signal Average"
3. Drag and Drop.
4. Connect the inputs as displayed.
