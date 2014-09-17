on *:signal:Cy-EEG: {
  inc %Cy.X
  if (%Cy.X > 500) { 
    dec %Cy.X %Cy.X
    drawrect -f @Cy 1 1 0 0 $window(@Cy).w $window(@Cy).h 
  }
  var %Cy.index 0
  var %Cy.str = $gettok($1-,0,32)
  while (%Cy.index < %Cy.str) {
    inc %Cy.index
    var %Cy.data = $gettok($1-,%Cy.index,32)
    var %Cy.newXY = $calc((%Cy.index * 50) + (%Cy.data / 3.1) - 2800)
    var %Cy.oldXY = $calc((%Cy.index * 50) + ($gettok(%Cy.oldData,%Cy.index,32) / 3.1) - 2800)
    drawline -i @Cy %Cy.index 1 %Cy.X %Cy.newXY %Cy.X %Cy.oldXY
  }
  set %Cy.oldData $1-
  drawdot @Cy
}
