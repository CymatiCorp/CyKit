on *:signal:Cy-EEG: {

  if ($calc($ticks - %lastTick) > 10) { 
    set %lastTick $ticks
    return 
  }

  set %lastTick $ticks


  inc %Cy.X

  if (%Cy.X > $calc($window(@Cy).w - 20)) { 
    dec %Cy.X %Cy.X
    drawrect -fr @Cy $rgb(25,25,25) 1 0 0 $window(@Cy).w $window(@Cy).h 

  }


  var %Cy.index 0
  var %Cy.str = $gettok($1-,0,46)

  while (%Cy.index < %Cy.str) {
    inc %Cy.index

    var %order $calc((%cy.index * 40) + 10);

    set %Cy.data. [ $+ [ %cy.index ] ] $abs($gettok($1-,%Cy.index,46))
    set %Cy.DataOld. [ $+ [ %cy.index ] ] $abs($gettok(%Cy.OldData,%Cy.index,46))

    set %Cy.sel $abs(%Cy.data. [ $+ [ %cy.index ] ])
    set %Cy.SelOld $abs(%Cy.DataOld. [ $+ [ %cy.index ] ])

    dec %Cy.sel %cy.avg. [ $+ [ %cy.index ] ]
    dec %Cy.selOld %cy.avg. [ $+ [ %cy.index ] ]

    var %Cy.newY = $calc(%Cy.sel /4))
    var %Cy.oldY = $calc(%Cy.SelOld /4))

    inc %cy.newY %order
    inc %cy.oldY %order


    drawline @Cy %cy.index 1 %Cy.X %Cy.newY %Cy.X %Cy.oldY
    ; drawdot -i @Cy %cy.index 1 %Cy.X %Cy.newY 


  }
  set %Cy.OldData $1-
  drawdot @Cy
}

alias set_baseline {
  var %cy.index 0
  while (%cy.index < 14) {
    inc %cy.index

    inc  %cy.avg. [ $+ [ %cy.index ] ] %cy.data. [ $+ [ %cy.index ] ]
    set  %cy.avg. [ $+ [ %cy.index ] ] $calc(%cy.avg. [ $+ [ %cy.index ] ] /2)
  }
}
