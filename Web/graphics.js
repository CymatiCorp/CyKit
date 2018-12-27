/*

   CyKIT
   graphics.js   2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   Custom Graphics Functions for CyInterface.js
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
*/

//  Canvas Resizing.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function resizeCanvas() {
        
    cyCanvas.width   = (document.getElementById('canvasPane').offsetWidth );
    cyCanvas.height  = (document.getElementById('canvasPane').offsetHeight);
    canvasWidth      = cyCanvas.width;
    canvasHeight     = cyCanvas.height;
    buffer.width     = canvasWidth;
    buffer.height    = canvasHeight;
    var inc_step     = (canvasHeight / (260));
    var inc_y_offset = 5;
    cy_x         = canvasWidth -3;
    oldx         = cy_x -1;

    //if (typeof eegData[0]  == 'undefined' || selected_model == 0) { return; }
    
    refresh_pong();
    
    eeg_total = 14;
    if (typeof selected_model != 'undefined') {
        
        if (selected_model == 4 || selected_model == 3) {
            eeg_total = 5;
        }
    }

    for (i = 0; i < eeg_total; i++) {
        inc_y_offset +=  inc_step;

        eegData[i].style.top = Math.abs(parseFloat(inc_y_offset)) + "%";

        if (eeg_total == 5) {
            contactObj = document.getElementById('qualityID.' + sensorNAME['insight'][i]);
            eegData[i].style.height = (canvasHeight / 14);
        }
        else {
            contactObj = document.getElementById('qualityID.' + sensorNAME['epoc'][i]);
            eegData[i].style.height = (canvasHeight / eeg_total);

        }
        if (i > eeg_total) {
            eegData[i].style.visibility = "hidden";
        }
        else {
            eegData[i].style.visibility = "visible";
        }
        eegData[i].style.backgroundColor = color_palette[color_theme][i];
    }
    update_gyro_sliders();
}


//  Draw Dot. (Plot Data)
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function drawdot(contact, offset, x, y, color) {
    x = Math.round(x);
    oldx = Math.round(oldx)
    ctx.beginPath();
    ctx.lineWidth= line_size;
    ctx.strokeStyle=color;
    ctx.moveTo(oldx +1, y + offset);
    ctx.lineTo(x, oldy[contact]);
    ctx.stroke();
    oldy[contact] = y + offset;
}

//  Draw Line.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯
function drawLine(startX, startY, endX, endY, strokeStyle, lineWidth) {
    if (strokeStyle != null) { ctx.strokeStyle = strokeStyle; }
    if (lineWidth != null) { ctx.lineWidth = lineWidth; }
    
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.stroke();
    ctx.closePath();    
}
        
//  Scroll Screen.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function scroll_screen() { 

// When resuming testing for EPOC+ --- remove 1 at time.
    //cyCanvas.width   = (document.getElementById('canvasPane').offsetWidth -4);
    //cyCanvas.height  = (document.getElementById('canvasPane').offsetHeight);
   canvasWidth      = parseInt(cyCanvas.width);
   //canvasHeight     = parseInt(cyCanvas.height);
    
    //buffer.width     = canvasWidth -1;
    //buffer.height    = canvasHeight;
    
  if (scroll_check) {
        
        slow_scroll = slow_scroll + 2;  
        
        if (slow_scroll > 2) {
            
            slow_scroll = 0;
            btx.drawImage(cyCanvas, 0, 0, canvasWidth, canvasHeight);
            ctx.drawImage(buffer, -1, 0, (canvasWidth), canvasHeight);
            
            btx.fillStyle = (color_theme == 4 ? "#ffffff" : "#111111");
            btx.fillRect(0, 0, buffer.width, buffer.height);                  
           //btx.drawImage(graphPattern, 0, 0, buffer.width, buffer.height);
           //btx.fillRect(0, 0, canvasWidth, canvasHeight);
           //buffer.getContext('2d').clearRect(0,0,canvasWidth,canvasHeight);
           //buffer.getContext('2d').drawImage(graphImage,0,0);
        }
    }
}


//  Moves Line Segment Forward.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function move_data_forward() {
    /*
    cyCanvas.width   = (document.getElementById('canvasPane').offsetWidth  -5);
    cyCanvas.height  = (document.getElementById('canvasPane').offsetHeight -5);
    canvasWidth      = cyCanvas.width;
    canvasHeight     = cyCanvas.height;
    buffer.width     = canvasWidth;
    buffer.height    = canvasHeight;
   */
   //console.log(parseInt(cy_x) + " > " + canvasWidth);

    //console.log(cyCanvas.width);
    scroll_screen();
    if (scroll_check) {
        cy_x = canvasWidth -5;
        oldx = cy_x;
        return;
    }
    else {
        // .1 bluetooth insight
        cy_x += .1;
        oldx = cy_x;
        
        if (parseInt(cy_x) > canvasWidth) { 
            oldx = 0;
            cy_x = 0;
            ctx.clearRect(0, 0, canvasWidth, canvasHeight);
        }
    }
    
}
