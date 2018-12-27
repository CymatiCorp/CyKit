/*

   CyKIT
   play_sound.js -  2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   Sound for user interface.
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯

 */

var sound_disabled = false;
var beep_1 = new Audio(".\\Sounds\\beep_1.mp3");
var beep_2 = new Audio(".\\Sounds\\beep_2.mp3");
var beep_down = 0;
var active_beep = 0;

    beep_1.canPlayType('audio/mp3; codecs="mp3"');
    beep_2.canPlayType('audio/mp3; codecs="mp3"');

    
function play_beep(beep_type) {
    if (sound_disabled == true) { return; }
    eval("beep_" + beep_type).volume = 0.05;
    //eval("beep_" + beep_type).currentTime = 0;
    eval("beep_" + beep_type).play();
    beep_down = 0;
    active_beep = beep_type;
    fader();
}


function fader() {
    if (active_beep == 0) { return; }
    
    if (beep_down == 0) {
        if ((eval("beep_" + active_beep).volume + .05) > 0.9) {
            beep_down = 1;
        }
        else {
            eval("beep_" + active_beep).volume = eval("beep_" + active_beep).volume + .05;
        }
    }
    else {
        
        if ((eval("beep_" + active_beep).volume - 0.05) < 0.05) { 
            eval("beep_" + active_beep).volume = 0.0001;
            eval("beep_" + active_beep).stop;
            beep_down = -1;
            active_beep = 0;
            
        }
        else {
            eval("beep_" + active_beep).volume = eval("beep_" + active_beep).volume - .05;
        }
        
    }
    
    
}

//setInterval(fader, 10);
