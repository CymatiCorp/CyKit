;
;    CyKit 1.0 - eeg for mIRC.
;    ________________________
;
; *  Extract CyKit to a folder.
;
; *  Connect emotiv headset
; 
; *  Run Python.exe stream.py
;
;            or RunStream.bat 
;
; *  Load these files to mIRC rCyes 
;
;      /load -rs CyClient.mrc
;      /load -rs CySignal.mrc
; 
;  * /eeg 
; 
menu status  {
  EEG: eeg
  Reset Baseline: .timer 20 3 set_baseline
}

alias eeg {
  window -p @Cy -1 -1 500 700
  clear @Cy

  unset %cy.*
  set %Cy.X 0

  if ($sock(CyKit)) { 
    echo -s ::: Socket in Use.
    return
  }
  sockopen CyKit 127.0.0.1 5555
}

on *:sockopen:CyKit: {
  echo -s ::: CyKit ::: Connected.
  .timer 20 3 set_baseline
}
on *:sockclose:CyKit: {
  echo -s ::: CyKit ::: Disconnected.
}
on *:sockread:CyKit: {
  sockread -f %Cy.read
    .signal -n Cy-EEG %Cy.read
}
on *:close:@Cy: {
  sockclose CyKit
  echo -s ::: CyKit ::: Disconnected.
}

on *:unload: { 
  sockclose CyKit 
  unset -w %Cy.*
}
