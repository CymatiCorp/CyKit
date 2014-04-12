; RunStream.bat (stream.py)
;  Load this to mIRC remotes 
;  /load -rs emotClient.mrc  
;  /eclient 
;       to run.   
;
;  A picture window will show the active data nodes blinking.
;
;  Will update later.

alias eclient {
  sockopen ecc 127.0.0.1 50008
}

alias vgraph {
  window -epa @vgraph -1 -1 500 500
  ; Left Hemisphere
  set %NC.AF3 150 30 
  set %NC.F3 180 45

  set %NC.F7 120 50 
  set %NC.FC5 110 70
  set %NC.T7 120 120 
  set %NC.P7 140 150 
  set %NC.O1 190 180

  ;Right Hemisphere
  set %NC.AF4 280 30 
  set %NC.F4 250 45

  set %NC.F8 310 50 
  set %NC.FC6 320 70
  set %NC.T8 310 120 
  set %NC.P8 290 150 
  set %NC.O2 240 180
  ; NC = Node Coords

  set %nodes AF3 F3 F7 FC5 T7 P7 O1 AF4 F4 F8 FC6 T8 P8 O2 

  drawfill @vgraph 1 2 1 1
  var %i 0
  while (%i < $gettok(%nodes,0,32)) {
    inc %i
    drawdot @vgraph 15 10 %NC. [ $+ [ $gettok(%nodes,%i,32) ] ]

  }
}

on *:sockopen:ecc: {
  echo -s :: Connected! 
  egraph
}

on *:sockread:ecc: {
  sockread -f %ecc

  var %i 0
  var %s = $gettok(%ecc,0,32)
  while (%i < %s) {
    inc %i
    var %dataColor = $gettok(%ecc,%i,32)

    drawdot -r @vgraph %dataColor 10 %NC. [ $+ [ $gettok(%nodes,%i,32) ] ]
  }
}
