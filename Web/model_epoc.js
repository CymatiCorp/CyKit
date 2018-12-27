/*
    CyKIT
    model_epoc.js -  2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   [EPOC 1.0] Headset Model
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
 */

function verify_script() { return "epoc"; }
    
function process_EEG_data() {

    oldx = cy_x;
    if (scroll_check) {
        cy_x = canvasWidth -1; 
    }
    else {
        cy_x += 1;
    }
        
    if (cy_x > canvasWidth) { 
        oldx = 0;
        cy_x = 0; 
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    }

    if (battery_check == 127) {
        var myBattery = document.getElementById("CyBattery");
        var battery_percent = ((((parseInt(contact[0]) - 255) +31) *3.23));
        myBattery.innerHTML = parseInt(battery_percent)  + "%";
    }
    battery_check = contact[0];
    
    if (checkBaseline == true) {
        reset_counter += 1;
        
        if (reset_counter > 55) {
            reset_baseline = true;  
            reset_counter = 0;
        }
        
    }
    
    if (baseline[2] == null || reset_baseline == true) {
       
        if (baseline[2] != null && toggled == false) { 
         toggled = true;
         setTimeout(function() { toggle_baseline(false) }, 16000);
        }
        
        for (i = 0; i < contact.length; i++) {
            if (init_baseline == true) {
                baseline[i] = baseline[i] + Math.abs(contact[i]);
                baseline[i] = parseInt((baseline[i] / 2));
            }
            else {
                baseline[i] = Math.abs(contact[i]);
            }
        }
        
        init_baseline = false;
        reset_baseline = false;
    }               
        
    if (manualControl) {
        var myContact = document.getElementById("CySelect").value;
        var myValue = Math.abs(contact[myContact]);
        
        drawdot(myContact, 10, cy_x, ((eval(myValue) - baseline[myContact]) * eeg_resolution) , "white");
    }
    else {
        var inc_y_offset = 10;
        var inc_step = (contact.length +1);
        var arr_element;
        
        for (arr_element in sensorNAME['epoc']) {
            var c = document.getElementById("e." + sensorNAME['epoc'][arr_element]);
            var myColor = color_palette[color_theme][arr_element];
            var select_contact = (sensorDATA['epoc'][arr_element] -1)
            if (c.checked == true) {
                inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
                var value_data = (baseline[select_contact] - contact[select_contact]);
                var value_floor = 30;
                //var value_floor = Math.floor((baseline[select_contact] / 1000.0)) -10;
                //drawdot(select_contact, inc_y_offset, cy_x, value_floor - ((value_data * .128) *- (2 + eeg_resolution)) * eeg_resolution, myColor);
                drawdot(arr_element, inc_y_offset, cy_x, (value_floor - (value_data * .51) *- (eeg_resolution)), myColor);
             
            }
        }
    }

}