OpenViBE 0.14.0 
===============

Cykit sends 14 channels of data in the range of -8900 to 8900.<br>
As a Signed Integer Big-Endian format, in a continuous stream<br>
with no terminating characters.<br><br>
Connect to a localhost port above 1024 and below 32000<br>

* Start Cyos.py (or RunCyos.bat)<br>
 `Python.exe Cyos.py 127.0.0.1 5555`

``` or download and run win32 Executable here ```

Cyos (OpenViBE TCP Server - Revision 1.0 - Win32 Executable)<br>
http://cymaticorp.com/edu/github/Cyos-0.1.0.win32.py2.7.zip <br>


* Install OpenViBE - http://openvibe.inria.fr/downloads/

* Start Acquisition Server.

* Start OpenViBE Designer.

* Open C:\Program files\OpenViBE\share\openvibe\applications\acquisition-server\interface.ui
```
Navigate to line 53 and edit the '4' digit, to a '1'
 like so:
       <col id="0" translatable="yes">1</col> 
```

Edit Acquisition Server preferences with the following parameters.

   * As `Driver` choose `Generic Raw Telnet Reader`.
   * Set the `Connection port` as `4444` and `Sample count per sent block` as `1`. - Connects to OpenViBE port.
   * In `Driver Properties`, set
     * `Number of channels`: `14`
     * `Sampling frequency`: `128`
     * `Telnet host name`: `localhost`
     * `Telnet host port`: `5555` - Connects to CyKit Port.
     * `Endianness`: `Big endian`
     * `Sample type`: `16 bits SIGNED integer`
     * `Skip at start (bytes)`: `0`
     * `Skip at header (bytes)`: `0`
     * `Skip at footer (bytes)`: `0`
     
   * Click `Connect`
   * Click `Play` (it should display `Sending...`)

Click "Connect" on the OpenVIBE Acquisition server.

1. Verify the Log will say "Connection succeeded!"
2. Verify Data is being read from the Python Cyos.py server.

<img src='http://cymaticorp.com/edu/openvibe/acquire5.png' width=100% height=100%></img>
Figure A.

1. Run "OpenVIBE Designer"
2. Drag and drop "Acquisition Client" from Boxes (on the right) to the white window space on the left.
3. Drag and drop "Signal display" as well.
4. Hover over the pink arrow. "Signal Stream [signal]" drag a line from that arrow<br>
   to the green arrow "Signal [streamed matrix]" until a line connects them.
5. Double click "Acquisition Client"
6. Replace server hostname with "localhost"
7. Replace server port with your designated OpenVIBE port. (IE 4444)
8. Apply.


* Return to the "OpenVIBE acquisition server" and press "Play"

<img src='http://cymaticorp.com/edu/openvibe/acquire6.png' width=100% height=100%></img>
Figure B.

1. Return to the "OpenVIBE Designer" and press "Play"


1. A window will appear with your EEG stream.
2. Press Stop when completed or making signal changes.

<img src='http://cymaticorp.com/edu/matrix.png' width=100% height=100%></img>
Figure C.

Additionally, to smooth out your EEG data.

1. Select the line between "Acquisition client" and press delete.
  (or right click and delete.)
2. Find "Signal Processing > Averaging > Signal Average"
3. Drag and Drop.
4. Connect the inputs as displayed.
<img src='http://cymaticorp.com/edu/openvibe/acquire8.png' width=100% height=100%></img>
Figure D.
