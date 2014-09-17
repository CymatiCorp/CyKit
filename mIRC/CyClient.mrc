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

alias eeg { 
  set %Cy.X 0
  window -p @Cy -1 -1 500 700
  Cy 
  .enable #Cy-EEG
}
alias Cy {
  set %Cy.FPS 1023

  .disable #Cy-EEG

  if ($sock(CyKit)) { 
    echo -s ::: Socket in Use.
    return
  }
  sockopen CyKit 127.0.0.1 16031
}

on *:sockopen:CyKit: {
  echo -s ::: Connected!
}

on *:sockread:CyKit: {
  sockread -f %Cy.read
  var %Cy.Segment $calc($gettok(%Cy.read,0,32) /14)
  var %Cy.i 0
  while (%Cy.i < %Cy.Segment) {
    inc %Cy.i 
    var %Cy.a = $calc(14 * (%Cy.i -1) +1) 
    var %Cy.b = $calc(14 * (%Cy.i -1) +14)
    var %Cy.c = $gettok(%Cy.read, %Cy.a - %Cy.b ,32) 
    ; --- Module Calls ---
    .signal -n Cy-EEG %Cy.c
  }
}

on *:unload: { 
  sockclose CyKit 
  unset -w %Cy.*
}
