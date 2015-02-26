OpenViBE 0.14.0 
===============

Updated February 25, 2015<br>
CyKit is now working please note that it sends Signed Integer data now.<br>
You will have to make the appropriate changes in the acquisition server.<br>
This is done to accomdate emotiv's potential of giving -8900 to 8900 integer data.<br>

* Start Cyos.py (or RunCyos.bat)<br>
 `Python.exe Cyos.py 127.0.0.1 21555`

* Install OpenViBE - http://openvibe.inria.fr/downloads/

* Start Acquisition Server.

* Start OpenViBE Designer.

* Open C:\Program files\OpenViBE\share\openvibe\applications\acquisition-server\interface.ui

Navigate to line 53 and edit the '4' digit, to a '1'
 like so:
        <col id="0" translatable="yes">1</col>


Edit Acquisition Server preferences with the following parameters.

   * As `Driver` choose `Generic Raw Telnet Reader`.
   * Set the `Connection port` as `4444` and `Sample count per sent block` as `1`. - Connects to OpenViBE port.
   * In `Driver Properties`, set
     * `Number of channels`: `14`
     * `Sampling frequency`: `128`
     * `Telnet host name`: `localhost`
     * `Telnet host port`: `21555` - Connects to CyKit Port.
     * `Endianness`: `Big endian`
     * `Sample type`: `16 bits SIGNED integer`
     * `Skip at start (bytes)`: `0`
     * `Skip at header (bytes)`: `0`
     * `Skip at footer (bytes)`: `0`
     
   * Click `Connect`
   * Click `Play` (it should display `Sending...`)
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

1. Run the following :
``` 
hemokit-dump.exe --format sensorbytes --serve 127.0.0.1 4444
```
2. Click "Connect" on the OpenVIBE Acquisition server.


<img src='http://blueskynet.org/edu/openvibe/acquire4.png' width=100% height=100%></img>
Figure D.

1. Verify the Log will say "Connection succeeded!"
2. Verify Data is being read from the Python Cyos.py server.

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
