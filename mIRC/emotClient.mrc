;
;    emot 1.0 - eeg for mIRC.
;    ________________________
;
; *  Extract emotKit to a folder.
;
; *  Connect emotiv headset
; 
; *  Run Python.exe stream.py
;
;            or RunStream.bat 
;
; *  Load these files to mIRC remotes 
;
;      /load -rs emotClient.mrc
;      /load -rs emotSignal.mrc
; 
;  * /emot
;       to run.   

alias emot {
  if ($sock(emotKit)) { sockclose emotKit }
  sockopen emotKit 127.0.0.1 21013
  set %uGr 0
}

on *:sockopen:emotKit: {
  echo -s ::: Connected!
  window -p @emot -1 -1 500 700
}

on *:sockread:emotKit: {
  sockread -f %emot.read
  var %emot.Segment $calc($gettok(%emot.read,0,32) /14)
  var %emot.i 0
  while (%emot.i < %emot.Segment) {
    inc %emot.i 
    var %emot.a = $calc(14 * (%emot.i -1) +1) 
    var %emot.b = $calc(14 * (%emot.i -1) +14)
    .signal -n emotkit $gettok(%emot.read, %emot.a - %emot.b ,32)  
  }
}
