OpenViBE 0.14.0 
===============

Until I can sort out the issues with my CyKit's TCP server, <br>
I will refer you to a solution utilized by the hemokit project. <br>
(ie. emokit written in haskell).<br>
https://github.com/nh2/hemokit <br><br>

Download the latest version of hemokit-dump.exe 
https://github.com/nh2/hemokit/releases

Install OpenViBE
http://openvibe.inria.fr/downloads/

Start Acquisition Server.
Start OpenViBE Designer.

Open C:\Program files\OpenViBE\share\openvibe\applications\acquisition-server\interface.ui

Navigate to line 53 and edit the '4' digit, to a '1'
 like so: <br><br>
        ```
        <col id="0" translatable="yes">1</col>
        ```
<br><br>

Start the acquisition server with the following parameters.

   * As `Driver` choose `Generic Raw Telnet Reader`.
   * Set the `Connection port` as `4444` and `Sample count per sent block` as `1`.
   * In `Driver Properties`, set
     * `Number of channels`: `14`
     * `Sampling frequency`: `128`
     * `Telnet host name`: `localhost`
     * `Telnet host port`: `21555`
     * `Endianness`: `Big endian`
     * `Sample type`: `16 bits unsigned integer`
     * `Skip at start (bytes)`: `0`
     * `Skip at header (bytes)`: `0`
     * `Skip at footer (bytes)`: `0`
     * `Under Change channel names, make sure the channels 1 to 14 map to, in this order:`

    `F3, FC5, AF3, F7, T7, P7, O1, O2, P8, T8, F8, AF4, FC6, F4`

   * Click `Connect`
   * Click `Play` (it should display `Sending...`)

1. Run the following :
``` 
hemokit-dump.exe --format sensorbytes --serve 127.0.0.1:21555
```
1. Click "Connect" on the OpenVIBE Acquisition server.
2. Verify the Log will say "Connection succeeded!"

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
