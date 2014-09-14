on *:signal:emotKit: {
  inc %emot.X
  if (%emot.X > 500) { 
    dec %emot.X %emot.X
    drawrect -f @emot 1 1 0 0 $window(@emot).w $window(@emot).h 
  }
  var %emot.index 0
  var %emot.str = $gettok($1-,0,32)
  while (%emot.index < %emot.str) {
    inc %emot.index
    var %emot.data = $gettok($1-,%emot.index,32)
    var %emot.newXY = $calc((%emot.index * 50) + (%emot.data / 3.1) - 2800)
    var %emot.oldXY = $calc((%emot.index * 50) + ($gettok(%emot.oldData,%emot.index,32) / 3.1) - 2800)
    drawline -i @emot %emot.index 1 %emot.X %emot.newXY %emot.X %emot.oldXY
  }
  set %emot.oldData $1-
  drawdot @emot
}
