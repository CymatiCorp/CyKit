; RunStream.bat 
;
;  Load this to mIRC remotes 
;  /load -rs emotClient.mrc  
;  /eclient 
;       to run.   
;
;  A picture window will show the active data nodes blinking.
;
; /eclient  - eeg graph
; /optwin   - training options
; /rec_     - begin training.


alias rec_ {
  inc %training
  set %segment 0
  hmake $+(train,%training) 100
}

alias optwin {
  window -p @options -1 -1 500 500
  drawrect @options 
}


alias vgraph {
  window -ep @vgraph -1 -1 500 500
  window -p @ugraph -1 -1 500 800

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

  set %nodes AF3 F7 F3 FC5 T7 P7 O1 O2 P8 T8 FC6 F4 F8 AF4 

  drawfill @vgraph 1 2 1 1

  var %i 0
  while (%i < $gettok(%nodes,0,32)) {
    inc %i
    drawdot -i @vgraph 15 10 %NC. [ $+ [ $gettok(%nodes,%i,32) ] ]

  }
}
alias eclient {
  sockopen ecc 127.0.0.1 25013
  set %uGr 0
}
on *:sockopen:ecc: {
  echo -s :: Connected! 
  unset %ND.*
  unset %NA
  vgraph
}

on *:sockread:ecc: {
  sockread -f %ecc
  var %totalSegments $calc($gettok(%ecc,0,32) /14)

  if ($chr(46) isin %totalSegments) { return }

  var %i 0
  while (%i < %totalsegments) {
    inc %i 
    var %a = $calc(14 * (%i -1) +1) 
    var %b = $calc(14 * (%i -1) +14)
    ;  echo -s :: %totalsegments :: %a - %b  
    .signal -n emotkit $gettok(%ecc, %a - %b ,32)  
  }

}
