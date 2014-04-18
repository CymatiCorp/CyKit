on *:signal:emotkit: {
  inc %uGr
  if (%uGr > 500) { dec %uGr %uGr | 
    drawrect -f @ugraph 1 1 0 0 $window(@ugraph).w $window(@ugraph).h 
  }
  if ($hget($+(train,%training)) != $null) { 
    inc %segment 
    hadd $+(train,%training) %segment $1- 
  }
  var %i 0
  var %s = $gettok($1-,0,32)
  ; echo -s ::: %s
  ; echo -s ::: $base($gettok($1-,1,32),10,2,4)

  while (%i < %s) {
    inc %i
    var %zline = $gettok($1-,%i,32)
    var %dataLine = $left(%zline,2)
    var %Qline = $right(%zline,2)
    var %Mline = $calc(%zline - 800)
    var %dataColor $calc(%dataline * 25)
    ;  drawdot -r @vgraph %dataColor 10 %NC. [ $+ [ $gettok(%nodes,%i,32) ] ]

    ; drawdot  @ugraph %i 1 %uGr $calc( (%dataline + (%qline /2))  + ((%i * 30) -20) )
    drawdot  @ugraph %i 1 %uGr $calc((%i * 40) + (%dataline /.51) - (%qline /.5))

  }
  drawdot @ugraph
}
