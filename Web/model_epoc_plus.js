/*

   CyKIT
   model_epoc_plus.js -  2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   [EPOC+] Headset Model
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
 */
 
function verify_script()  { return "epoc_plus"; }

// Epoc+ 
// ¯¯¯¯¯¯¯

//  Battery Information for EPOC+.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
//  (format-0)  Battery_Level_Indiactor = 16th byte 
//  (format-1)  Battery_Level_Indiactor = 30th byte 
//
//   45-58  EPOC+ (16-bit) counter(0-127) on counter 127 [   16th byte]
//  92-117  EPOC+ (16-bit) counter(0-255) on counter 255 [   16th byte]
// 220-245  EPOC+ (14-bit) counter(0-127) on counter 128 [counter byte]

function process_EEG_data() {
    //Check Battery Level.   
    
    // This section needs reworked, to work with the new system of acquiring the devices "sample rate"  from the config.
    // Battery will only report correctly for 128hz.
    
    if (contact[1] == "16") {
        if (no_battery == false && no_counter == false) {
             if (formatType == 0) { var battery_position = 16; } else { var battery_position = 30; }
            //if (contact[
            if (contact[0] == 127 || contact[0] == 255) {
                
                // max battery = 117
                // (very low battery < 99)
                //console.log("blev=" + contact[battery_position]);
                
                if (contact[battery_position] < 64) {
                    hz_mode = 128;
                    battery_mode = 0;
                }
                else {
                    hz_mode = 256;
                    battery_mode = 117;
                }
                
                
                if (contact[battery_position] != 0) {
                     console.log(battery_position + " " + contact[battery_position] + " "  + contact[30] + " " + contact[31]); 
                     
                     //var battery_percent = (((parseInt(contact[battery_position]) - 117) +25) *3.85);
                      var battery_percent = ((parseInt(contact[battery_position]) - battery_mode)  * 1.612903); //128hz mode ---
                     //var battery_percent = (((parseInt(contact[battery_position]) - 117) +25)  * 3.85); //      255hz mode --- 
                     //var battery_percent = ((119.5 - parseInt(contact[battery_position])) * 1.612903);
                     var BatteryLevel = document.getElementById("CyBattery");
                         BatteryLevel.innerHTML = parseInt(battery_percent) + "%";
                
                }
            }
        }
    }
    
    var quality_id = qualityCOUNTER['epoc_128_highRes'][parseInt(contact[0])];
    
    if (CyFormat == "Floating Point") { 
        set_quality(quality_id, contact[17], contact[16]);
    }
    else {
        set_quality(quality_id, contact[31], contact[30]);
    }
    
    if (checkBaseline == true) { 
        reset_counter +=1;
        if (reset_counter > 55) {
            //Counter to Reset Baseline.
            reset_baseline = true;  
            reset_counter = 0;
        
            if (baseline[2] != null && toggled == false) { 
               toggled = true;
               setTimeout(function() { toggle_baseline(false) }, 16000);
            }
        }
    }

    //console.log(contact[1]);
    //  Data Line.
    // ¯¯¯¯¯¯¯¯¯¯¯¯¯
    if (contact[1] == "16") {

        //  (Data Panel) for EEG Data.
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        
        if (document.getElementById("enable-EEG-View").checked == true && data_mode == 1) {
            printData += 1;
            if (printData > 55) {
                v = 0;
                for (var i = 0; i < (contact.length < 19 ? 14 : 32); i++) {
                        //gyroData[i] = document.getElementById('gyroData:' + i);
                    if (contact[i] == undefined)  {
                        eegData[i].style.visibility = "hidden";
                        continue;
                    }
                    else {
                        
                    //  eegData[i].style.visibility = "visible";
                    }
                    
                    if (formatType == 0) {
                        //console.log(i + " " + contact.length);
                        if ((i+2) < 16) { 
                            eegData[i].value = contact[i+2];
                            eegData[i].style.visibility = "visible";
                            
                            eegData[i].style.backgroundColor = color_palette[(color_theme == 4 ? 3 : color_theme)][i];
                        }
                    }
                    else {
                        /* Disabled for Raw Data Mode.
                        
                        if ((i+2) < 16) { 
                            eegData[i].style.visibility = "visible";
                            
                            select_contact = parseInt(sensorDATA[device_name][i]);
                            
                            eegData[i].value = convertEPOC_PLUS(contact[(select_contact +2)],contact[(select_contact+1)]);
                            eegData[i].style.backgroundColor = color_palette[(color_theme == 4 ? 3 : color_theme)][i];
                        }    
                        */
                        if (current_tab == "Calibration") {
                           gyroData[i].value = contact[i];
                        }
                        
                    }
                    
                }
            }
        }

        //  Epoc+ Data.   
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        //console.log("ManualControl=" + manualControl + " formatType = " + formatType);
        if (manualControl) {
            // Plot single Floating Point value.
            if (formatType == 0) {
                var optionValue = document.getElementById("CySelect").value;
                if (optionValue == "All Sensors") { return; }
                var selectedContact = parseInt(optionValue); 
                var myContact = parseInt(sensorDATA['epoc'][selectedContact]);
                var value_data = parseFloat(contact[myContact]);
                drawdot(myContact, 100, cy_x, (value_data - baseline[myContact]) * eeg_resolution, "111111");
            }

            //  Plot single Raw value.
            // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
            else {
                //if (contact.length < 32) { return; }
                var optionValue = document.getElementById("CySelect").value;
                if (optionValue == "All Sensors") { return; }
                var selectedContact = parseInt(optionValue);
                var myContact = selectedContact;
                
                var value_1 = contact[selectedContact];
                var value_2 = contact[(selectedContact +1)];
                var value_data = convertEPOC_PLUS(parseInt(value_1), parseInt(value_2));

                drawdot(myContact, 50, cy_x,(value_data - baseline[selectedContact]  * eeg_resolution), color_palette[color_theme][0]);
            }
        }
        else {
            //  Plot Multiple Float Point values.
            // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
            if (formatType == 0) {
                //console.log(color_theme);
                var arr_element;
                var inc_y_offset = 10;
                var inc_step = (sensorNAME['epoc'].length +3);
                
                for (arr_element in sensorNAME['epoc']) {
                    var c = document.getElementById("e." + sensorNAME['epoc'][arr_element]);
                    var myColor = color_palette[color_theme][arr_element];
                    inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
                    if (c.checked == true) {
                        select_contact = parseInt(sensorDATA['epoc'][arr_element]);
                        
                        var value_data = (baseline[select_contact] - parseFloat(contact[select_contact]));
                        var value_floor = Math.floor((baseline[select_contact] / 1000.0)) + 30;
                        if (document.getElementById("enable-EEG-View").checked == true) {
                            //eegData[arr_element].value = value_data;
                        }
                        if (document.getElementById("enable-singleWave").checked == true) { inc_y_offset = (canvasHeight / 2); }
                        drawdot(arr_element, inc_y_offset, cy_x, value_floor - ((value_data * .128)) * eeg_resolution, myColor);
                    }
                }
            }

            //  Plot Multiple Raw Data values.
            // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
            else {
                var inc_y_offset = 10;
                var inc_step = (sensorNAME['epoc'].length +3);
                var uv  = 1;
                v = 1;
                var value_floor = 30;
                for (var i = 2; i < (contact.length - (no_counter == true ? 0 : 0)); i+=2) {
                    uv += 1;
                    v +=1;
                    var c = document.getElementById("e." + sensorNAME['epoc'][v-2]);
                    if (c == null) {
                        continue;
                    }
                    var myColor = color_palette[color_theme][uv-2];
                    inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
                    if (c.checked == true) {
                        var value_1 = contact[i];
                        var value_2 = contact[(i +1)]; 
                        var value_data = convertEPOC_PLUS(parseInt(value_1), parseInt(value_2));
                            //value_floor = Math.floor(parseInt(baseline[uv]) / 1000);
                            value_floor += 5;
                        if (document.getElementById("enable-singleWave").checked == true) { inc_y_offset = (canvasHeight / 2); }
                        drawdot(uv-1, inc_y_offset, cy_x, value_floor - ((value_data * eeg_resolution) * .0128), myColor);
                    
                    }
                
                }
            }
        }
        
        
        //  Reset Baselines:::Epoc+
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        if (contact[1] == "16" || contact[1] == "32") {
            if (filter_enabled == true) {
                baseline = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                reset_baseline = false
                init_baseline = false
                return; 
            }
            
            if (baseline[2] == null || reset_baseline == true) {
                if (pyBaseline == true) { 
                    reset_baseline = false;
                    init_baseline = false;
                    return;
                }

                //  Manual Control (ON) -> (Single EEG Stream)
                // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                if (manualControl) {
                    if (formatType == 0) {
                        //  Baseline for Floating Point. (Single data stream)
                        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        i = myContact;
                        if (init_baseline == false) {
                            baseline[i] = baseline[i] + Math.abs(value_data) + 4201.02564096001;
                            baseline[i] = (baseline[i] / 3);
                        }
                        else {
                            baseline[i] = Math.abs(value_data);
                        }
                    }
                    else {
                        //  Baseline for Raw Data integers. (Single data stream)
                        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        if (init_baseline == true) {
                            baseline[i] = baseline[i] + Math.abs(value_data);
                            baseline[i] = parseInt((baseline[i] / 2));
                        }
                        else {
                            baseline[i] = Math.abs(value_data);
                        }
                    }
                }
                else {
                    //  Manual Control (OFF) -> (Multiple EEG Streams)
                    // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                    if (formatType == 0) {
                        //  Baseline for Floating Point. (Multiple EEG Streams)
                        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                        device_name = headset[selected_model].replace('epoc_plus','epoc');
            
                        for (arr_element in sensorNAME[device_name]) {
                            select_contact = parseInt(sensorDATA[device_name][arr_element])

                            if (init_baseline == true) {
                                baseline[select_contact] = baseline[select_contact] + parseFloat(contact[select_contact]) + 4201.02564096001;
                                baseline[select_contact] = (baseline[select_contact] / 3);
                            }
                            else {
                                baseline[select_contact] = Math.abs(parseFloat(contact[select_contact]));
                            }
                        }
                    }  
                    else {
                            //  Baseline for Raw Data Integers. (Multiple EEG Streams)
                            // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                            for (var i = 0; i < 33; i++) {
                                if (init_baseline == true) {
                                    baseline[i] = baseline[i] + Math.abs(value_data);
                                    baseline[i] = parseInt((baseline[i] / 2));
                                }
                                else {
                                    baseline[i] = Math.abs(value_data);
                                }
                            }
                        }
                } //End Manual Control.
            }
            reset_baseline = false;
            init_baseline = false;

        }
        
    move_data_forward();
   }
   
   
}

function process_Gyro_data() {

    //  Epoc+ Gyro
    // ¯¯¯¯¯¯¯¯¯¯¯¯¯
    
    // Consider calibration menu (or baseline button) 
    // to get a head-front orientation and acquire baseline.
    
    if (contact[1] == "32") {
        // Reset Baseline for Gyro mode
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        
        if (parseInt(baseline[2]) > 255) { baseline = []; }
        
        if (baseline[2] == null) { 
            for (var i = 0; i < 32; i++) {
                baseline[i] = cartesian(parseInt(contact[i])) + 255;
            }
        }
        
        gyro_counter += .01;
        
        if (gyro_counter < 2) {
            
            for (var i = 0; i < 32; i++) {
                if (baseline[i] != null) {
                    
                var select_gyro = gyroDATA['eplus_gyro'][(i*2-1)];
                    
                    if (reset_counter > 2.9) {
                        //baseline[select_gyro] = baseline[select_gyro] + (cartesian((parseInt(contact[select_gyro]))) * .02);
                    }
                    if (i > 6 && i < 10) {
                        //baseline[select_gyro] = parseInt((((parseInt(baseline[select_gyro])) +127) /2));
                        baseline[select_gyro] = ((parseInt(baseline[select_gyro]) +127) / 2);
                        
                    }
                    else {
                        baseline[i] = parseInt(baseline[i]) + parseInt(contact[i]);
                        baseline[i] = parseInt((parseInt(baseline[i]) / 2));
                    }
                }
                else {
                    baseline[i] = parseInt(contact[i]);
                }
                
             
            }
            
            gyro_counter = 0;
        }
        
        if (current_tab == "Gyro" || current_tab == "Game") {
            
            // Gyro / Accelerometer
            // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
            for (i = 1; i < 7; i++) {
                var select_gyro = gyroDATA['eplus_gyro'][((i*2-1))];

                var gyro_value = cartesian(parseInt(contact[select_gyro]));
                
                var gyroObj = document.getElementById('sliderID.' + (i-1));
                    gyroObj.value = gyro_value -127;

                var labelObj = document.getElementById('label2.' + (i-1));
                    labelObj.innerHTML = cartesian(contact[select_gyro]);

                check_range((i-1));
            }

            // Magnetometer
            // ¯¯¯¯¯¯¯¯¯¯¯¯¯
            for (i = 7; i < 10; i++) {
                
                var select_gyro = gyroDATA['eplus_gyro'][(i*2-1)];

                var labelObj = document.getElementById('label2.' + (i-1));
                    labelObj.innerHTML = (parseInt(cartesian(parseInt(contact[select_gyro]))) - 127) *25;
                
                var gyroObj = document.getElementById('sliderID.' + (i-1));
                    gyroObj.value = (parseInt(cartesian(parseInt(contact[select_gyro]))) - 127) *25;
               
               check_range((i-1)); 
            }
            
        }
        
        var inc_y_offset = 10;
        var inc_step = (contact.length +3);
        var value_1 = (contact[2] * .128205128205129); 
        var value_2 = contact[3];
        
        var value_data = cartesian(parseInt(value_2) + value_1);
            drawdot(i, inc_y_offset, cy_x, value_data * eeg_resolution, myColor);
        
        
        //  (Data Panel) for Gyro Data and Raw Data.
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        if (document.getElementById("enable-Gyro-View").checked == true && data_mode == 2) {
            printData += 1;
            if (printData > 55) {
                    v = -2;
                for (var i = 0; i < 32; i++) {
                        //gyroData[i] = document.getElementById('gyroData:' + i);
                    if (contact[i] == undefined)  {
                        gyroData[i].style.visibility = "hidden";
                    continue;
                    }
                    gyroData[i].value = contact[i];
                    gyroData[i].style.visibility = "visible";                            
                    
                }
            }
        }
    }
}