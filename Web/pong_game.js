/*

   CyKIT
   pong_game.js -  2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   Browser Pong game for CyKIT
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
 */
var mouse = {};
var ball_game = null;
var gameStarted = false;
var gameReady = 0;
var ball_inc_x = 0;
var ball_inc_y = 0;
var ball_x = 0;
var ball_y = 0;
var newPlayerY = 0;
var fastLoop = 0;
var player2fastLoop = null;
var player2Loop = null;
var gyro_check = null;
var slowlydrag = 0;
var inc_paddle_speed = 0;
//import { color_palette, play_beep, color_theme, triggered } from './js'
//import * as CyInterface from "./js" 

gamePane.addEventListener("mousemove", trackPosition, true);

function trackPosition(e) {
	if (document.getElementById("gameSync").checked == true) { return; }
    mouse.x = e.pageX;
	mouse.y = e.pageY;
}

function refresh_pong() {
    if (gameStarted == true) {
        console.log(color_theme);
        var gamePane = document.getElementById('gamePane');
        var player_1 = document.getElementById('player_1');
        var player_2 = document.getElementById('player_2');
            player_1.setAttribute("style", "position:absolute; left:30px; top:" + (gamePane.offsetHeight /2.5) + "px; width:10px; height:18%;  background: repeating-linear-gradient(55deg," + color_palette[(color_theme + 1) % 3][7] + ",#fff 5px,#aaa 2px,#465298 20px)");
            player_2.setAttribute("style", "position:absolute; right:30px; top:" + (gamePane.offsetHeight /2.5) + "px; width:10px; height:18%;  background: repeating-linear-gradient(55deg," + color_palette[(color_theme + 1) % 3][7] + ",#fff 5px,#aaa 20px,#465298 20px)");
    }
    
}

function change_game_state(readyState) {
    gameReady = readyState;
}

function start_game() {
    play_beep(1);
    gameStarted = true;
    gameReady = 1;
    document.getElementById('gameStart').style.visibility = "hidden";
    document.getElementById('player_ready').style.visible = "visible";
    document.getElementById('player_ready').style.color = color_palette[color_theme][1];
    
    document.getElementById('player_1_score').style.visible = "visible";
    document.getElementById('player_2_score').style.visible = "visible";
    document.getElementById('player_1_score').style.color = color_palette[color_theme][1];
    document.getElementById('player_2_score').style.color = color_palette[color_theme][1];
    
    mouse.y = parseInt((document.getElementById('gamePane').offsetHeight));
    ball_game    = setInterval( function x() { game_loop();  }, 5);
    player2Loop = setInterval( function y() { player2_loop();  }, 250);
}

//  Game Loop
// ¯¯¯¯¯¯¯¯¯¯¯¯
function game_loop() {
  	
    if (document.getElementById('gameSync').checked == true) { 
        
        var gamePaneHeight = document.getElementById('gamePane');
        
        if (triggered[3] == -1) {
            if (mouse.y < (gamePaneHeight.offsetHeight + gamePaneHeight.offsetTop)) { 
                slowlydrag = slowlydrag - 1;
                if (inc_paddle_speed < 0) { inc_paddle_speed = 2; }
                if (slowlydrag < -1) { 
                    slowlydrag = -1; 
                    inc_paddle_speed = 2;
                }
                    
                mouse.y = mouse.y +1 + inc_paddle_speed;
            }
            
        }

        if (triggered[3] == 0) {
            inc_paddle_speed = 0;
            slowlydrag = slowlydrag + 1;
            if (slowlydrag > 5) {
                
                if (mouse.y > parseInt((gamePaneHeight.offsetHeight /2) + parseInt(gamePaneHeight.offsetTop))) { mouse.y = mouse.y - 1; }
                if (mouse.y < parseInt((gamePaneHeight.offsetHeight /2) + (gamePaneHeight.offsetTop))) { mouse.y = mouse.y + 1; }
                slowlydrag = 0;
            }
        }

        if (triggered[3] == 1) {
            if (mouse.y > gamePaneHeight.offsetTop) {
             slowlydrag = slowlydrag - 1;
             if (inc_paddle_speed > 0) { inc_paddle_speed = -2; }
             if (slowlydrag < -1) { 
                    slowlydrag = -1; 
                    inc_paddle_speed = -2;
                }
                mouse.y = mouse.y -1 + inc_paddle_speed;
            }
        }
        
    }
    if (gameStarted == false) { 
        document.getElementById('gameStart').style.visibility = "visible";
        return; 
    }
    
    var gamePane = document.getElementById('gamePane');
    var player_1_score = document.getElementById('player_1_score');
    var player_2_score = document.getElementById('player_2_score');
    var player_1 = document.getElementById('player_1');
    var player_2 = document.getElementById('player_2');
    var ball = document.getElementById('ball');
    
    // Create Player 1
    if (player_1 == null) {
        var player_1 = gamePane.appendChild(document.createElement("DIV"));
            player_1.setAttribute("id", "player_1");
            player_1.setAttribute("style", "position:absolute; left:30px; top: " + (gamePane.offsetHeight /2.5) + "px; width:10px; height:18%;  background: repeating-linear-gradient(55deg," + color_palette[(color_theme + 1) % 3][7] + ",#fff 5px,#aaa 2px,#465298 20px)");
            
            }
    // Create Player 2
    if (player_2 == null) {
        var player_2 = document.getElementById('gamePane').appendChild(document.createElement("DIV"));
            player_2.setAttribute("id", "player_2");
            player_2.setAttribute("style", "position:absolute; right:30px; top:" + (gamePane.offsetHeight /2.5) + "px; width:10px; height:18%;  background: repeating-linear-gradient(55deg," + color_palette[(color_theme + 1) % 3][7] + ",#fff 5px,#aaa 20px,#465298 20px)");
            // background-color: " + color_palette[(color_theme +1) % 3][7]);
    }

    if (ball == null) {
        
        var ball = document.getElementById('gamePane').appendChild(document.createElement("DIV"));
            ball.setAttribute("id","ball");
            ball.setAttribute("style", "position:absolute; left:" + (gamePane.offsetWidth /2.04) + "px; top:" + (gamePane.offsetHeight /2.1) + "px; width:10px;" +
            "border-radius:15px; border: 12px solid #" + ((color_theme * 15) + (color_theme * 15) + (color_theme * 155)) );
        
        var ball_x = ball.style.left;
        var ball_y = ball.style.top;
        
    }
    
    
    //gamrReady states.
    // < 0 = Countdown
    //   1 = Initialize Game
    //   2 = In-game
    
    if (gameReady < 0) { return; }
    
    if (gameReady == 1) { 
        //Choose Ball Direction.
        mouse.y = parseInt((document.getElementById('gamePane').offsetHeight));
        
        if (parseInt(Math.random() * 2) == 1) {
            ball_inc_x = -1;
        }
        else {
            ball_inc_x = 1;
        }
        
        for (var i = 0; i < parseInt((Math.random() * 100)); i++) {
            ball_inc_y = parseInt((Math.random() * 3) +1);
        }
        gameReady = 2;
    }
    if (newPlayerY < player_2.offsetTop) {
            player_2.style.top = parseInt(player_2.style.top) - 2;
    }
    
    if (newPlayerY > player_2.offsetTop) {
            player_2.style.top = parseInt(player_2.style.top) + 2;
    }
    if(mouse.y) {
        player_1.style.top = (mouse.y - gamePane.offsetTop - 15);
    }	
    
    ball_x = parseInt(ball.style.left) + parseInt(ball_inc_x);
    ball_y = parseInt(ball.style.top) +  parseInt(ball_inc_y);
    
        
    if ((ball.offsetTop + 25) > gamePane.offsetHeight) {       
        if (ball_inc_y > 0.0) {  ball_inc_y = - (ball_inc_y); }
    }
    
    if ((ball.offsetTop) < gamePane.style.top) {
        if (ball_inc_y < 0.0) {  ball_inc_y = -(ball_inc_y); }
    }
    
    if ((ball.offsetLeft + 20) > gamePane.offsetWidth -5) {       
        player_1_score.innerHTML = parseInt(player_1_score.innerHTML) + 1;
        ball_x = (gamePane.offsetWidth /2.04);
        ball_y = (gamePane.offsetHeight /2.1);
        gameReady = 1;
    }
    
    if ((ball.offsetLeft) < gamePane.style.left) {
        player_2_score.innerHTML = parseInt(player_2_score.innerHTML) + 1;
        gameReady = 1;
        ball_x = (gamePane.offsetWidth /2.04);
        ball_y = (gamePane.offsetHeight /2.1);
        //if (ball_inc_x < 0.0) {  ball_inc_x = -(ball_inc_x); }
    }
   
   if (gameReady == 2) {
    
    if ((ball.offsetLeft +2) < (player_1.offsetLeft + 10)) {
        
        if ((ball.offsetTop + 11) >= player_1.offsetTop && (ball.offsetTop + 11) <= (player_1.offsetTop + player_1.offsetHeight)) {
         ball_inc_x = -(ball_inc_x);
         ball_x = parseInt(ball.style.left) + parseInt(ball_inc_x) +4;
         
        }
    }
    if ((ball.offsetLeft +18) > (player_2.offsetLeft -2)) {
        //console.log("COLLIDE 1!");     
        
        if ((ball.offsetTop + 11) >= player_2.offsetTop && (ball.offsetTop + 11) <= (player_2.offsetTop + player_2.offsetHeight)) {
        //console.log("COLLIDE 2!");     

        ball_inc_x = -(ball_inc_x);
         ball_x = parseInt(ball.style.left) + parseInt(ball_inc_x) -4;
         
        }
    }
    }
    
    ball.style.left = ball_x + "px";
    ball.style.top  = ball_y + "px";
    
}

function player2_loop() {
var player_2 = document.getElementById('player_2');
var ball = document.getElementById('ball');
var gamePane = document.getElementById('gamePane');
    
    if (player_2 != null) {
        
        if (fastLoop == 0) {
            if (ball_inc_x > 0) {
                if (ball.offsetLeft > parseInt(gamePane.offsetWidth / 1.5)) { 
                    if (player2Loop != null) { 
                        clearInterval(player2Loop);
                        player2fastLoop = setInterval( function z() { player2_loop(); }, 10);
                        console.log(player2fastLoop);
                        fastLoop = 1;
                    }
                }
            }
        }
        else {
            if (ball_inc_x < 0) {
                if (player2fastLoop != null) {
                    clearInterval(player2fastLoop);
                    player2Loop = setInterval( function m() { player2_loop();  }, 250);
                    fastLoop = 0;
                }
            }
        }
        
        
        if ((ball.offsetLeft + parseInt(Math.random() * 100)  > (gamePane.offsetWidth /2)) && ball_inc_x > 0) {
        
            if (ball_inc_x < 0) { 
                    if (parseInt(Math.random() * 2) > 0) {
                        newPlayerY = parseInt(parseInt(gamePane.offsetHeight /2.4) - (Math.random() *10));
                    }
                    else {
                        newPlayerY = parseInt((Math.random() *20) + parseInt(gamePane.offsetHeight /2.4));
                 }
            }
                                
        
            if (parseInt(Math.random() * 2) > 0) {
                newPlayerY = parseInt((ball.offsetTop +5) - (Math.random() * 25) -45);
                //console.log(newPlayerY);
                //player_2.style.top = ball.offsetTop;
            }
        }
        else {
            if (ball_inc_x < 0) { 
              
                 newPlayerY = parseInt(gamePane.offsetHeight /2.4);
            }
            
        }
    }
}


function game_round() {
    
}

