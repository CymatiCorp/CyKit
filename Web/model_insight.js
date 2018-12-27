/*

   CyKIT
   model_insight.js -  2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   [Insight] Headset Model
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
 */

function verify_script()  { return "insight"; }

function process_EEG_data() {

    if (baseline[1] == null || reset_baseline == true) {
        for (i = 0; i < 33; i++) {
            baseline[i] = contact[i];
        }
        reset_baseline = false;
    }
    device_name = headset[selected_model].replace('epoc_plus','epoc');
    if (bluetooth != "") {
        device_name = "bt_" + device_name;
    }   //format-1 for bt_Insight
    if (battery_check == 127) {
        reset_baseline = true;
        var counter = parseInt(contact[0]);
        var myBattery = document.getElementById("CyBattery");
        var battery_percent = (((counter - 245) +26) *3.85);
        myBattery.innerHTML = parseInt(battery_percent) + "%";
    }

    battery_check = contact[0];

    /*
    if (cy_x > canvasWidth) { 
        oldx = 0;
        cy_x = 0; 
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    }
    */
    if (battery_check < 128) {
        quality_id = qualityCOUNTER['insight'][parseInt(contact[0])];
        
        //console.log(contact);
        if (device_name == "bt_insight") {
            set_insight_quality(quality_id, contact[11], -1);
        }
        else {
            set_insight_quality(quality_id, parseInt(contact[15]), parseInt(contact[16]));
        }
    }
                
    if (manualControl) {
        var myContact = document.getElementById("CySelect").value;
        var currentValue = eval(contact[myContact]) - 127;
        var myColor = "white";
        var subtract_by = 255;

        drawdot(myContact, 60, cy_x, (currentValue - baseline[myContact]) * eeg_resolution, myColor);
    }
    else {
        var arr_element;
        var inc_y_offset = 50;
        var inc_step = (sensorNAME['insight'].length +1);
        
        for (arr_element in sensorNAME['insight']) {
            var c = document.getElementById("i." + sensorNAME['insight'][arr_element]);
            var myColor = color_palette[color_theme][arr_element];
            inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
            if (c.checked == true) {
                select_contact = parseInt(sensorDATA[device_name][arr_element]);
                var value_data = (parseFloat(contact[select_contact]) * .51);
                var value_floor = (parseFloat(contact[select_contact +1]) * .0128);;
                
                drawdot(arr_element, inc_y_offset, cy_x, (value_floor - (value_data)) * eeg_resolution * 2 + 50, myColor);
                eegData[arr_element].value = convertEPOC_PLUS(contact[select_contact +1],contact[select_contact]);
            }
        }
        
        // Insight Gyro
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯
        if (current_tab == "Gyro") {
        
            // Gyro / Accelerometer
            for (i = 1; i < 7; i++) {
                var gyro_value = (contact[gyroDATA['insight'][(i*2)-2]] - 127);
                if (gyro_baseline[(i-1)] == null) { gyro_baseline[(i-1)] = 0; }
                    gyro_baseline[(i-1)] = gyro_value;
                var gyroObj = document.getElementById('sliderID.' + (i-1));
                    gyroObj.value = gyro_baseline[(i-1)];
            }
            
            // Magnetometer
            for (i = 7; i < 10; i++) {
                
                //var gyro_value1 = (contact[gyroDATA["insight"][(i*2)-2]]);
                var gyro_value1 = (((baseline[gyroDATA['insight'][(i*2)-2]]) - (contact[gyroDATA['insight'][(i*2)-2]])) * 15);
                var gyro_value2 =    (contact[gyroDATA['insight'][(i*2)-1]]);
                //gyro_baseline[(i-1)] = parseInt((gyro_value2) * .8);
                
                //var labelObj = document.getElementById('label.' + (i-1));
                //    labelObj.innerHTML = gyro_value1;
                
                var labelObj = document.getElementById('label2.' + (i-1));
                    labelObj.innerHTML = gyro_value1;
                
                var gyroObj = document.getElementById('sliderID.' + (i-1));
                    gyroObj.value = parseInt(mag1(gyro_value1));
            }
        }
        
        /*
        var arr_element;
        for (arr_element in sensorNAME['insight']) {
            var c = document.getElementById("i." + sensorNAME['insight'][arr_element]);
            var myColor = color_palette[arr_element];
            if (c.checked == true) {
                var currentValue = contact[sensorDATA_insight[arr_element]];
                offset = (((canvasHeight + 22) / sensorNAME['insight'].length) * (arr_element)) + 30;
                drawdot(arr_element, offset, cy_x, (cy_y - baseline[arr_element]) * .3, myColor);
            }
        }
        */
    }
    move_data_forward();
}