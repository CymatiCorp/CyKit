on *:signal:Cy-EEG: {

  inc %Cy.X

  if (%Cy.X > 500) { 
    dec %Cy.X %Cy.X
    drawrect -f @Cy 1 1 0 0 $window(@Cy).w $window(@Cy).h 

  }
  var %Cy.index 0
  var %Cy.str = $gettok($1-,0,46)

  while (%Cy.index < %Cy.str) {
    inc %Cy.index

    var %order $calc(%Cy.index * 30)

    var %Cy.data = $gettok($1-,%Cy.index,46)
    var %Cy.newY = $abs($calc(%Cy.data / 3.1))
    var %Cy.oldY = $abs($calc($gettok(%Cy.oldData,%Cy.index,46) / 3.1))

    inc %Cy.newY %order
    inc %Cy.oldY %order

    drawline -i @Cy %cy.index 1 %Cy.X %Cy.newY %Cy.X %Cy.oldY
    ;  titlebar @cy %cy.index 1 %Cy.X %Cy.newY %Cy.X %Cy.oldY

  }
  set %Cy.oldData $1-
  drawdot @Cy

}
