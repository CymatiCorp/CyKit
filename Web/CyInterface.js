/*

   CyKIT
   CyInterface.js   2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   CyKIT HTML back-end for controlling interface and handling data.
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
 */

//  Socket Variables.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
var cyHost = document.getElementById('cyHost').value;
var cyPort = document.getElementById('cyPort').value;
if (cyHost == null) { var cyHost = "127.0.0.1"; }
if (cyPort == null) { var cyPort = "55555"; }
var client = new CySocketClient(cyHost, cyPort, "CyKITv2");

            
//  Canvas Variables.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
var cyCanvas = document.getElementById('cyCanvas');
var ctx = cyCanvas.getContext('2d');
var buffer = document.createElement('canvas');
var btx = buffer.getContext('2d');
    buffer.width = (document.getElementById('cyCanvas').offsetWidth);
    buffer.height = (document.getElementById('cyCanvas').offsetHeight);
    ctx.imageSmoothingEnabled = false;
    btx.imageSmoothingEnabled = false;
var img = document.getElementById('graphImage');
var graphPattern = btx.createPattern(img, "repeat");
    btx.fillStyle = graphPattern;

var logWindow = document.getElementById("logWindow").appendChild(document.createElement('iframe'));
    logWindow.src = "../py3/EEG-Logs";
    logWindow.id = "logFiles";
    logWindow.width = "100% ";
    logWindow.height = "100%";

var logWindow = document.getElementById("logFiles")
    console.log(logWindow);
    logWindow.style = "resize:both; overflow: auto; font-color: white;";

//  Initialize Variables.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
var current_theme  = null;
var color_theme    = 4;
var line_size      = ".6";
var canvasWidth    = cyCanvas.width;
var canvasHeight   = cyCanvas.height;
var selected_model = 0;
var no_battery     = false;
var no_counter     = false;
var bluetooth      = "";
var data_mode      = 0;
var toggled        = false;
var baseline_check = true;
var pyBaseline     = true;
var delimiter      = ",";
var viewType       = "16";     // Default:: (16 = Data)           (32 = Gyro)
var formatType     = 0;     //  Default:: (0  = Floating Point) (1  = Raw Data)
var mems_x         = 100;
var battery_check  = 0;
var reset_baseline = true;
var init_baseline  = true;
var gyro_baseline  = [];
var baseline       = [];
var current_tab    = "EEG";
var eeg_resolution = 1;
var eegData        = [];
var gyroSlider     = [];
var minRange       = [];
var maxRange       = [];
var triggered      = [];
var qualityData    = [];
var device_name    = "";
var EEG_View       = null;
var battery_mode   = 54.5;
var hz_mode        = 128;
var eeg_total      = 14;
var filter_enabled = false;
var scriptLoaded   = null;          // Used for loading headsets dynamically.
var contact        = ""; 
var CyFormat       = document.getElementById("CyFormat").value;
var manualControl  = false;
var checkBaseline  = document.getElementById("CyBaseline").checked;
var pyBaseline     = document.getElementById("PyBaseline").checked;

        
//  Initialize Local Variables.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
//var myContact      = 1;
var myResult       = 0;
var cy_x           = 1;
var cy_y           = 10;
var oldx           = 0;
var oldy           = [];
var oldg           = [];
var reset_counter  = 0;
var gyro_counter   = 0;
var printData      = 0;
var v              = 0;
var slow_scroll    = 0;
var scroll_check   = document.getElementById("CyScroll").checked;
var baseline_check = document.getElementById("CyBaseline").checked;
var eeg_resolution = (document.getElementById("myRange").value * .01);

var modelTypes = ['None','Epoc-Research','Epoc','Insight (Research)','Insight','Epoc+ (Research)','Epoc+', 'EPOC+ (14-bit)', 'Epoc-Flex'];
var headset = { 
                0: 'epoc', 1: 'epoc', 2: 'epoc', 3: 'insight', 4: 'insight', 5: 'epoc_plus', 6: 'epoc_plus', 7:'epoc_plus', 8: 'epoc_flex'  }

var sensorNAME = {
                    epoc: ['AF3','F7','F3','FC5','T7','P7','O1','O2','P8','T8','FC6','F4','F8','AF4'],
                 insight: ['AF3','T7','Pz', 'T8', 'AF4'] }
                 
var sensorDATA = {
                    epoc: [4,5,2,3,6,7,8,9,10,11,14,15,12,13],
                 insight: [5,9,13,23,27],
              bt_insight: [1,3,5,7,9] }

var gyroDATA = {
                   insight: [1,2,3,4,7,8,11,12,19,20,21,22,25,26,29,30,31,32,33,34],
                eplus_gyro: [2,3, 4,5, 6,7, 8,9, 10,11, 12,13, 14,15, 16,17, 30,31]

                              
                    
                }
              

var qualityDIV = { 'F3': 2, 'FC5': 3, 'AF3': 0, 'F7': 1, 'T7': 4, 'P7': 5, 'O1': 6, 'O2': 7, 'P8': 8, 'T8': 9, 'F8': 12, 'AF4': 13, 'FC6': 10, 'F4': 11 }

//  EPOC+ Quality Counters. (loRes/hiRes) Changes how often sensors are updated.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
var qualityCOUNTER = { 
                    
                    insight: ['','','AF3','','T7','','Pz','','','T8','','AF4','','','','','','','','',
                              '','','','','','','','','','','','','','','','','','','','',
                              '','','','','','','','','','','','','','','','','','','','',
                              '','','','','','','AF3','','T7','','Pz','','','T8','','AF4','','','','',
                              '','','','','','','','','','','','','','','','','','','','',
                              '','','','','','','','','','','','','','','','','','','','',
                              '','','','AF4','','','',''],
                          
                    epoc_128_highRes: ['F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4',
                               'F8','AF4','','','','','','','','','','','','','','','','','','','','','','',
                               '','','','','','','','','','','','','','','','','','','','','','','','','',
                               '','F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4',
                               'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                               'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                               'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                               'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                               'F8',''],
                               
                    epoc_128_lowRes: ['F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4',
                               'F8','AF4','','','','','','','','','','','','','','','','','','','','','','',
                               '','','','','','','','','','','','','','','','','','','','','','','','','',
                               '','F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4',
                               'F8','AF4','','','','','','','','','','',
                               '','','','','','','','','','','','',
                               '','','','','','','','','','','','',
                               '','','','','','','','','','','','',
                               '',''],
                                     
                    epoc_256_highRes: ['F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4', 
                                     'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4',
                                     'FC6','F4','F8','AF4','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','','',
                                     'F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4',
                                     'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4',
                                     'FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                                     'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4',
                                     'FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                                     'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4',
                                     'FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                                     'F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4',
                                     'FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4','F8','AF4','FC6','F4',
                                     '',''],
                                     
                    epoc_256_lowRes: ['F3','FC5','AF3','F7','T7','P7','O1','O2','P8','T8','F8','AF4','FC6','F4', 
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','F3','FC5','AF3','F7','T7','P7', 
                                     'O1','O2','P8','T8','F8','AF4','FC6','F4','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','','','','','','','','','','','','','','','','','','','','','','','',
                                     '','','']

}

                
var color_palette  = {
                            0: ['#ff7f7f','#ffbe7f', '#ffdf7f', '#dfff7f','#a0ff7f','#7fffdf','#7fdfff',
                                '#7fa0ff','#a07fff', '#df7fff', '#ff7fdf','#ff7fa0','#ff7f7f','#fdff7f'],
                            1: ['#ff0000','#ff8000', '#ffbf00', '#bfff00','#40ff00','#00ffbf','#00bfff',
                                '#0040ff','#4000ff', '#bf00ff', '#ff00bf','#ff0040','#ff0000','#ffff00'],
                            4: ['#000','#000', '#000', '#000','#000','#000','#000',
                                '#000','#000', '#000', '#000','#000','#000','#000'],
                            3: ['#999','#999', '#999', '#999','#999','#999','#999',
                                '#999','#999', '#999', '#999','#999','#999','#999'], 
                            2: ['#fff','#fff', '#fff', '#fff','#fff','#fff','#fff',
                                '#fff','#fff', '#fff', '#fff','#fff','#fff','#fff'] }
                                            

var quality_palette = {     
                            0: ['#333','#ff0000','#ee5000','#66ea8d'],
                            1: ['#333','#ff0000','#ee5000','#66ea8d'],
                            2: ['#333','#ff0000','#ee5000','#66ea8d'],
                            3: ['#333','#ff0000','#ee5000','#00c0ff'],
                            4: ['#333','#ff0000','#ee5000','#00c0ff']
}

var themes = [ "cyBlue", "cyGray", "cyScientific" ]

create_quality(14, 'epoc');
setTimeout(function() { resizeCanvas() }, 500);

//  Calibration Gyro Values.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
var gyroData = [];
for (var i = 0; i < 32; i++) {
    gyroData[i] = document.getElementById('gyroData').appendChild(document.createElement("INPUT"));
    gyroData[i].setAttribute("type", "text");
    gyroData[i].style = "width:100px; font-size:10px;";
}

//  Open Tab for Button.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
for (var i = 0; i < 8; i++) { 
    document.getElementById("tab." + i).onclick = function(e) { 
        openTab(this.innerHTML);
    }
}



// Rounding Function.
function roundToTwo(num) {    
    return +(Math.round(num + "e+2")  + "e-2");
}

function update_gyro_sliders() {
    if (gyroSlider[1] == null) { create_gyro_sliders(); }
    var gyroWidth = document.getElementById('gyroPane').clientWidth;
    
    var m = -1;
    var inc_m = 0;
    for (var i = 0; i < 9; i++) {
        
        m = m + 1;
        if (m == 3) { 
            m = 0; 
            inc_m += 6;
        }

        var location_x = (gyroWidth / 9);
        document.getElementById('a_rangeID.'  + i).style.left  = (i * 9) + 9.5   + inc_m  + "%";
        document.getElementById('b_rangeID.'  + i).style.left  = (i * 9) + 9.5   + inc_m  + "%";
        document.getElementById('sliderID.' + i).style.left    = (i * 9) + 7.5   + inc_m  + "%";
        document.getElementById('label.'    + i).style.left    = (i * 9) + 7.5   + inc_m  + "%";
        document.getElementById('label2.'   + i).style.left    = (i * 9) + 7.5   + inc_m  + "%";
        check_range(i);
    }

}



function create_gyro_sliders() {
    
    var location_x = 0;
    var gyroText          = ["X","Y","Z","X","Y","Z","X","Y","Z"];
    var gyroStyle         = ["red-slider","red-slider","red-slider","green-slider","green-slider","green-slider","blue-slider","blue-slider","blue-slider"];
    var gyroColor         = ["#333","#333","#333","#777","#777","#777","#ddd","#ddd","#ddd"];
    var gyroWidth = document.getElementById('gyroPane').canvasWidth;
    // Gyro Sliders
    // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    for (var i = 0; i < 9; i++) {
            location_x = (50 + (i * (canvasWidth / 9)));
            gyroSlider[i] = document.getElementById('gyroPane').appendChild(document.createElement("INPUT"));
            gyroSlider[i].setAttribute("class","slider");
            gyroSlider[i].setAttribute("id","sliderID." + i);
            gyroSlider[i].setAttribute("type","range");
            gyroSlider[i].setAttribute("min","-127");
            gyroSlider[i].setAttribute("max","127");
            gyroSlider[i].setAttribute("value","0");
            //gyroSlider[i].setAttribute("oninput","move_gyroSlider(this.value)");
            gyroSlider[i].setAttribute("style","position:absolute; left:" + (location_x + 20) + "px; top: 180px; height: 10px;  width: 250px; margin: 0; transform-origin: 75px 75px; transform: rotate(-90deg); background-color:" + gyroColor[i] + ";");
        
        var gyroLabel = document.getElementById('gyroPane').appendChild(document.createElement("LABEL"));
            gyroLabel.setAttribute("style","position:absolute; left:" + (location_x +20)+ "px; top: 330px;");
            gyroLabel.setAttribute("id","label." + i);
            gyroLabel.classList.add(gyroStyle[i]);
            gyroLabel.innerHTML = gyroText[i];
            gyroLabel = document.getElementById('gyroPane').appendChild(document.createElement("LABEL"));
            gyroLabel.setAttribute("style","position:absolute; left:" + (location_x +20)+ "px; top: 390px;");
            gyroLabel.setAttribute("id","label2." + i);
            
            gyroLabel.classList.add(gyroStyle[i]);
            gyroLabel.innerHTML = "";
            
        var gyroRange = document.getElementById('gyroPane').appendChild(document.createElement("DIV"));
            gyroRange.setAttribute("id","a_rangeID." + i);
            gyroRange.setAttribute("style","position:absolute; width:6px; opacity: .5; top: 153px; left:" + parseInt(location_x -12)  + "px; height:50px; background-color:#ffffff;");
            minRange[i] = 50;
            
            gyroRange = document.getElementById('gyroPane').appendChild(document.createElement("DIV"));
            gyroRange.setAttribute("id","b_rangeID." + i);
            gyroRange.setAttribute("style","position:absolute; width:6px; opacity: .5; top: 206px; left:" + parseInt(location_x +24)  + "px; height:50px; background-color:#ffffff;");
            maxRange[i] = -50;
            triggered[i] = 0;
    }
    
}

function check_range(select_slider) {
    if (document.getElementById("RangeTriggers").checked == false) { return; }
    
    var check_gyro = document.getElementById("sliderID." + select_slider);
    
    if (check_gyro == null) { return; }
    
    if (check_gyro.value > minRange[select_slider]) { 
        document.getElementById("a_rangeID." + select_slider).style.backgroundColor = "#00ff00";
        triggered[select_slider] = 1;
        return;
    }
    else {
        document.getElementById("a_rangeID." + select_slider).style.backgroundColor = "#ffffff";
        triggered[select_slider] = 0;
    }
    
    if (check_gyro.value < maxRange[select_slider]) { 
        document.getElementById("b_rangeID." + select_slider).style.backgroundColor = "#00ff00";
        triggered[select_slider] = -1;
    }
    else {
        document.getElementById("b_rangeID." + select_slider).style.backgroundColor = "#ffffff";
        triggered[select_slider] = 0;
    }
    
}

// Update Sensor Selection Combobox.
function update_sensorList(select_headset) {
    
    var sensorList = document.getElementById("CySelect");

    var i = 0;
    for(i = sensorList.length - 1 ; i >= 0 ; i--) {
        sensorList.remove(i);
    }
    
    var sensorOption = document.createElement("option");
    sensorOption.text = "All Sensors";
    sensorList.add(sensorOption);
    
    
        if (formatType == 0) {
            for (i = 0; i < sensorNAME[select_headset].length; i++) {
                var sensorOption = document.createElement("option");
                sensorOption.text = sensorNAME[select_headset][i];
                sensorOption.value = i;
                sensorList.add(sensorOption);
            }
        }
        else {
            for (i = 0; i < 33; i++) {
                var sensorOption = document.createElement("option");
                sensorOption.text = i;
                sensorOption.value = i;
                sensorList.add(sensorOption);
            }
        }

}

function create_quality(contact_length, headset_type) {
    //  Run-time Input Values for EPOC.
    // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    eegData = [];
    qualityData = [];
    var inc_y_offset = 5;
    var inc_step = 28
    var clearInput = document.getElementById('eegData');
    var clearQuality = document.getElementById('qualityPanel');
    
    while (clearQuality.firstChild) {
        clearQuality.removeChild(clearQuality.firstChild);
    }
    
    while (clearInput.firstChild) {
        clearInput.removeChild(clearInput.firstChild);
    }
    
    for (var i = 0; i < contact_length; i++) {
        eegData[i] = document.getElementById('eegData').appendChild(document.createElement("INPUT"));
        qualityData[i] = document.getElementById('qualityPanel').appendChild(document.createElement("DIV"));
        eegData[i].setAttribute("type", "text");
        eegData[i].style = "width:100px; height:0px; font-size:10px; display:block;";
        eegData[i].style.backgroundColor = color_palette[color_theme][i];
        //eegData[i].classList.add("tooltip");
        eegData[i].innerHTML = "<div class='tooltip'><span class='tooltiptext'><br> </span></div>";
        qualityData[i].innerHTML = "<div style='position:relative; padding: 0px 4px; top: -2px; width:15px; padding-top: 10px; height:" + 7 + "%; left: 2px; min-width:20px;'><div style='position:absolute; align=right; left:9px; top:15px; z-index:1; font-size:9px; color:white;'> " + sensorNAME[headset_type][i] + "</div><div id='qualityID." + sensorNAME[headset_type][i] + "' class='tooltip' style='min-height:15px; border-radius:15px; border: 12px solid #333;'><span class='tooltiptext' style='position:absolute; width:30px; left:45px;'>" + sensorNAME[headset_type][i] +" </span></div></div>";
        
        qualityData[i] = document.getElementById('qualityID.' + sensorNAME[headset_type][i])
        
        eegData[i].style.top = inc_y_offset + "px";
        
        inc_y_offset += Math.abs(parseInt((canvasHeight / inc_step)));
    }
}


function set_insight_quality(id, core_value, detail_value) { 
if (id == "" ||  id == null || typeof id == 'undefined') { return; }

    if (detail_value == -1) {
        //Insight - Bluetooth
        
        if (core_value < 50) { 
            quality_color = quality_palette[color_theme][0];         // black.
        }
        else {
            if (core_value < 160) {
                quality_color = quality_palette[color_theme][1];     // red.
            }
            else {
                if (core_value < 250) {
                    quality_color = quality_palette[color_theme][2]; // orange.
                }
                else {
                    quality_color = quality_palette[color_theme][3]; // green.
                }
            }
        }
    }
    else {
    set_color = "";
    //Insight - USB
        //new_value = parseFloat((core.value + "." + detail_value))
        //console.log(id);
        quality_color = quality_palette[color_theme][0]; // black.
        
        
        
        if (core_value > 2) { 
            if (core_value < 6) {
                quality_color = quality_palette[color_theme][2]; // orange.
                set_color = "orange";
            }
            else {
                quality_color = quality_palette[color_theme][3]; // green.
                set_color = "blue";
            }
            
        }
        else {
            if (detail_value > 49) { 
                quality_color = quality_palette[color_theme][1]; // red.
                set_color = "red";
            }
            if (core_value > 0 && detail_value > 30) {
                quality_color = quality_palette[color_theme][2]; // orange.
                set_color = "orange";
            }
        }
    }
    
    //if (id == "T7") {
    //    console.log("id." + id + " " + core_value + "." + detail_value + " = " + set_color);
    //}
    
    document.getElementById("qualityID." + id).style.border = "12px solid " + quality_color;
}

function set_quality(id, core_value, detail_value) { 
    if (id == "" || id == null || typeof id == 'undefined') { return; }
    //console.log(id);
    var quality_color = quality_palette[color_theme][0]; // black.
    if (core_value > 0) { 
        if (detail_value < 129) {
            quality_color = quality_palette[color_theme][2]; // orange.
            if (core_value > 1) {
                quality_color = quality_palette[color_theme][3]; // green.
            }
        }
        else {
            quality_color = quality_palette[color_theme][3]; // green.
        }
        
    }
    else {
        if (detail_value > 49) { 
            quality_color = quality_palette[color_theme][1]; // red.
        }
        if (detail_value > 158) {
            quality_color = quality_palette[color_theme][2]; // orange.
        }
    }
    
    document.getElementById("qualityID." + id).style.border = "12px solid " + quality_color;
}


//  Open Tab Menu.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function openTab(tabName) {
    
    current_tab = tabName;
    play_beep(2); // play_sound.js * 
    
    var i;
    var x = document.getElementsByClassName("tabs");
    
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    document.getElementById(tabName).style.display = "block"; 
    if (tabName != "Game") {
        change_game_state(-1);
    }
    else { 
        change_game_state(2);
    }
    
    if (tabName == "Gyro") {
        data_mode = 2;
        client.sendData("CyKITv2:::setDataMode:::" + 2);
        if (typeof gyroSlider != 'undefined') {
            if (gyroSlider[1] == null) { create_gyro_sliders(); }
        }
        
        document.getElementById("qualityPanel").style.display = "none";
        document.getElementById("EEG").style.display = "none"; 
        document.getElementById("canvasPane").style.width = "72%";
        document.getElementById("eegData").style.display = "none";
        document.getElementById("canvasPane").style.left = "20.5%";
        
        resizeCanvas();
        return;
    }
    
    if (tabName == "EEG") {
        data_mode = 1;
        client.sendData("CyKITv2:::setDataMode:::" + 1);
        document.getElementById("qualityPanel").style.display = "block";
        document.getElementById("sensorPane").style.display = "block";
        document.getElementById("canvasPane").style.width = "71.5%";
        document.getElementById("gyroData").style.display = "none";
        setTimeout(function() { resizeCanvas() }, 10);
      
     }  
     else {
       document.getElementById("qualityPanel").style.display = "none";
       document.getElementById("eegData").style.display = 
       (document.getElementById("enable-EEG-View").checked == true ? "block" : "none");
       document.getElementById("gyroData").style.display = 
       (document.getElementById("enable-Gyro-View").checked == true ? "block" : "none");
       
    }
    var CyFormat = document.getElementById("CyFormat").value;

    if (document.getElementById("enable-EEG-View").checked == true && CyFormat == "Floating Point") {
        document.getElementById("eegData").style.display = "block";
        document.getElementById("canvasPane").style.left = "27%";
        if (tabName == "Calibration") {
            document.getElementById("canvasPane").style.width = "47.5%";
        }
        else {
            document.getElementById("canvasPane").style.width = "71.5%";
        }
    } 
    else {
        document.getElementById("eegData").style.display = "none";
        document.getElementById("canvasPane").style.left = "20.5%";
        if (tabName == "Calibration") {
        document.getElementById("canvasPane").style.width = "54%";
       }
       else 
       {
            document.getElementById("canvasPane").style.width = "71.5%";
       }
    }

    if (tabName == "Calibration") {
        x[0].style.display = "block";
        client.sendData("CyKITv2:::setDataMode:::" + 1);
        document.getElementById("sensorPane").style.display = "none";
        document.getElementById("qualityPanel").style.display = "block";
        //if (document.getElementById("enable-EEG-View").checked == true) {
        //    document.getElementById("canvasPane").style.left = "20.5%";
        //}
        setTimeout(function() { resizeCanvas() }, 100);
        return;
    }
        
    setTimeout(function() { resizeCanvas() }, 100);

}

//  Theme Selection.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
for (var i = 1; i < 4; i++) {
    document.getElementById("theme." + i).onclick = function(e) { 
        setTheme(themes[(parseInt(this.id.split(".")[1]) -1)]); 
    }
}


//  Slider (Data Resolution).
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function changeSlider(info) {
    var eegRes = document.getElementById("CyRes");
        eegRes.innerHTML = "&nbsp&nbsp" + info + " %&nbsp&nbsp";
        eeg_resolution = (document.getElementById("myRange").value * .01);
        
       //var eeg_magnifier = (document.getElementById("myRange").value * .2);
       //resizeCanvas();
}

//  Data Mode Change. (EEG / Gyro).
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function changeDataMode(mode) {
    var CyDataMode = document.getElementById("dataMode").value;
    console.log(CyDataMode);
    if (CyDataMode == "EEG Data") {
        data_mode = 1;
    }
    else {
        data_mode = 2;
    }
    client.sendData("CyKITv2:::setDataMode:::" + data_mode);
    play_beep(1); // play_sound.js *
    
}

//  Data Format Change.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function changeFormat(format) {
    if (current_tab == "Gyro") { 
        baseline = [];
        document.getElementById("CyFormat").value = "Raw Data";
        return; 
    } 
    var changeBaseline = setInterval( function() { setTimeout(function() { toggle_baseline(true); }, 500); }, 15000);
    
    // Format 0 (Data sent as a float)
    // Format 1 (Data sent as unconverted values (to be converted by javascript))
    // Format 3 (Data is reformatted (strung together as binary and broken apart as 7 bits))
    var CyFormat = document.getElementById("CyFormat").value;
    if (CyFormat == "Floating Point") {
        if (selected_model == 4) {
            if (bluetooth == "bt") {
                formatType = 3;
            }
            else {
                formatType = 2;
            }
        }
        if (selected_model == 6) {
            formatType = 0;
            document.getElementById("eegData").style.display = "block";
            document.getElementById("canvasPane").style.left = "27%";
            if (current_tab == "Calibration") {
                document.getElementById("canvasPane").style.width = "47.5%";
            }
            else  {
                document.getElementById("canvasPane").style.width = "71.5%";
            }
        }
        
    }
    else {
        if (selected_model == 4) {
            if (bluetooth == "bt") {
                formatType = 3;
            }
            else {
                formatType = 3;
            }
        }
        if (selected_model == 6) {
            formatType = 1;
            document.getElementById("eegData").style.display = "none";
            document.getElementById("canvasPane").style.left = "20.5%";
            if (current_tab == "Calibration") {
            document.getElementById("canvasPane").style.width = "54%";
           }
           else 
           {
                document.getElementById("canvasPane").style.width = "71.5%";
           }
            //console.log("test2!!!");
        }
    
    }
    console.log("bluetooth = " + bluetooth);
    console.log("select model = " + selected_model);
    console.log("format type = " + formatType);
    client.sendData("CyKITv2:::changeFormat:::" + formatType);
    update_sensorList(headset[selected_model].replace('epoc_plus','epoc'));
}
    

//  Model Changing.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function modelChange(model) {
    if (client == null) { return; }
        console.log(model[model.selectedIndex].id);
        selected_model = model[model.selectedIndex].id;
        client.sendData("CyKITv2:::setModel:::" + selected_model);
    }

function refreshLog() {
    var logWindow = document.getElementById("logFiles");
        logWindow.src = "../py3/EEG-Logs";
}


document.getElementById('dataMode').onchange = function(e) {
    changeDataMode(this)
}

document.getElementById('resetBaseline').onclick = function(e) {
    setTimeout(function() { toggle_baseline(false) }, 100);
}
document.getElementById('myRange').oninput = function(e) {
    changeSlider(this.value)
}
document.getElementById('CySelect').onchange = function(e) {
    manualControl  = (document.getElementById("CySelect").value == "All Sensors") ? false : true; 
}
document.getElementById('CyFormat').onchange = function(e) {
    changeFormat(this);
}
document.getElementById('gameStart').onclick = function(e) {
    start_game();    
}
//  Record Start Button.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('cyStartRecord').onclick = function(e) {
    client.sendData("CyKITv2:::RecordStart:::" + document.getElementById('cyRecordFile').value); 
    play_beep(1); // play_sound.js *
}

//  Record Stop Button.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('cyStopRecord').onclick = function(e) {
    client.sendData("CyKITv2:::RecordStop");
    setTimeout(function() { refreshLog() }, 200);
    play_beep(1); // play_sound.js *
}

//  Connect Button.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('cyConnect').onclick = function(e) {

    var cyHost = document.getElementById('cyHost').value;
    var cyPort = document.getElementById('cyPort').value;

    if (cyHost == null) { var cyHost = "127.0.0.1"; }
    if (cyPort == null) { var cyPort = "55555"; }

    client.connect(cyHost, cyPort);
    play_beep(1); // play_sound.js *
}

//  Epoc+ Sample Setting.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('CySample').onclick = function(e) {
    update_settings_mode();    
    play_beep(1); // play_sound.js *
}

//  Epoc+ Sample Setting.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('CyGyro').onclick = function(e) {
    update_settings_mode();    
    play_beep(1); // play_sound.js *
}
 
//  Update Epoc+ Settings.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function update_settings_mode() {
    var cyMode = document.getElementById("CyMode");
    var cySample = document.getElementById("CySample");
    var cyGyro = document.getElementById("CyGyro");
    
    var Data_Gyro_Rate = { 0: [1,2,3,4], 1: [5,6,7,8] }

    if (cyMode.value == "Epoc+") {
        Cy_Settings_Mode = Data_Gyro_Rate[cySample.selectedIndex][cyGyro.selectedIndex];
        console.log(Cy_Settings_Mode);
    }

}

//  Reset Baseline. 
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function clearBaseline() {
    baseline = [];
}

//  Toggle Baseline Button.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function toggle_baseline(setbaseline) {
    reset_baseline = setbaseline
    document.getElementById("CyBaseline").checked = setbaseline;
    
    baseline_check = document.getElementById("CyBaseline").checked;
    pyBaseline = document.getElementById("PyBaseline").checked;
    
    client.sendData("CyKITv2:::setBaselineMode:::" + ((pyBaseline && baseline_check) ? 1 : 0));
    toggled = false;
}

//  Epoc+ Settings Mode.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('CyMode').onclick = function(e) {
    play_beep(1); // play_sound.js *
    var cyMode   = document.getElementById("CyMode");
    var cySample = document.getElementById("CySample");
    var cyGyro   = document.getElementById("CyGyro");
    
    if (cyMode.selectedOptions[0].id == "mode-EPOC") {
        cySample.disabled = true;
        cyGyro.disabled = true;
        var Cy_Settings_Mode = 0;
        cySample.selectedIndex = 0;
        cyGyro.selectedIndex = 1;
    }
    else {
        cySample.disabled = false
        cyGyro.disabled = false;
        Cy_Settings_Mode = 1;
        cySample.selectedIndex = 0;
        cyGyro.selectedIndex = 0;
    }
    play_beep(1); // play_sound.js *
}

// Connect Button.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('cyUpdateSetting').onclick = function(e) {

    var cyDevice = document.getElementById("CyDevice");
    if (cyDevice.innerHTML == "EPOC+") {
        if (Cy_Settings_Mode != null) {
            client.sendData("CyKITv2:::UpdateSettings:::" + Cy_Settings_Mode);
        }
    }
    play_beep(1); // play_sound.js *
}
// TODO: Send soft Disconnect. :::Disconnect

//  Disconnect Button.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('cyDisconnect').onclick = function(e) {

    var cyPicture = document.getElementById("CyKIT-picture");
    cyPicture.style.backgroundImage = "url('./images/CyKITv2-bg-off.png')";
    
    var selectEPOC = document.getElementById("selectEpocSensor");
    var selectINSIGHT = document.getElementById("selectInsightSensor");
    
    baseline = [];
    init_baseline = true;
    toggle_baseline(true);
    document.getElementById("CyHeadset").innerHTML = "None.";
    document.getElementById("CyStatus").innerHTML = "Not Connected.";
    document.getElementById("convertFormat").style.display = "block"; 
    selectEPOC.style.visibility = 'hidden';
    selectINSIGHT.style.visibility = 'hidden';
    client.sendData("CyKITv2:::Disconnect");
    //client.onClose();
    play_beep(1); // play_sound.js *
}

//  Mask Level Change. (Advanced)
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
document.getElementById('maskChange').onclick = function(e) {
    client.sendData("CyKITv2:::setMask:::" + document.getElementById('CyMask').value + ":::" + document.getElementById('newMask').value);
    reset_baseline = true;  
}


function timedResize() {    
    setTimeout(function() { resizeCanvas() }, 200);
}

function model_loaded(modelLoaded) {
    console.log(modelLoaded);
}


function mag1(value) { 
    if (value > 32) {
        return (value - 32);
    }
    else {
        return value;
    }
}

//  Plots Gyro Points In Cartesian Format.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function cartesian(value) {
      value = parseInt(value);
      if (value < 127) { 
        value =  value + 127; 
      }
      else {
        if (value > 127) { 
            value = value - 127; 
        }
      }
      return value;
}


document.getElementById("gyro-range").addEventListener("mousedown", clickGyroRange, true);

function clickGyroRange(e) {
// Update DIV range sliders when left clicked.

  var mouse_gyro_range = parseInt((e.pageY - document.getElementById("gyroPane").offsetTop - 80));
  var gyroRangeDivider = parseInt((document.getElementById("gyro-range").offsetHeight / 2));
  
        for (var i = 0; i < 9; i++) {
            var select_range_a = document.getElementById("a_rangeID." + i);
            var select_range_b = document.getElementById("b_rangeID." + i);

            if (select_range_a != null) {
                
                if (e.pageX > parseInt(select_range_a.offsetLeft + -20 + parseInt(document.getElementById("gyroPane").offsetLeft)) 
                 && e.pageX < parseInt(select_range_a.offsetLeft +  25 + parseInt(document.getElementById("gyroPane").offsetLeft))) {
                    
                 // Bottom (Max Range)
                  if (mouse_gyro_range > gyroRangeDivider) {
                    select_range_b.style.height = parseInt((mouse_gyro_range - gyroRangeDivider)) + "px";
                    maxRange[i] = (- parseInt((mouse_gyro_range - gyroRangeDivider)));

                   } //Top (Min Range)
                  else {
                    select_range_a.style.top    = (mouse_gyro_range +80) + "px";
                    select_range_a.style.height = parseInt((gyroRangeDivider - select_range_a.offsetTop) +80) + "px";
                    minRange[i] = parseInt((gyroRangeDivider - select_range_a.offsetTop) +80);

                  }

            }

        }

    }

}


//  Epoc+ EEG Data Decoding.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function convertEPOC_PLUS(value_1, value_2) {
    return (((value_1 * .128205128205129) + 4201.02564096001) + ((value_2 -128) * 32.82051289));
}
//  Epoc+ Gyro Data Decoding.
// ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
function convertEPOC_PLUS_gyro(value_1, value_2) {
    return ((8191.88296790168 + (value_1 * 1.00343814821 )) + ((value_2 - 128.00001) * 64.00318037383));
}


document.addEventListener("DOMContentLoaded", function(event) {

        //myScript.onload = impCode;
        //myScript.onreadystatechange = impCode;
        //document.body.appendChild(myScript);
        
        window.addEventListener('resize', timedResize, true);
        
        setInterval( function() { setTimeout(function() { toggle_baseline(true); }, 500); }, 15000);
        
        update_sensorList(headset[selected_model].replace('epoc_plus','epoc'));
        
        document.getElementById('CyMode').onclick();
        
        var check_sensor = document.getElementById("CySelect");
            check_sensor.addEventListener('change', function (event) {
                play_beep(1); // play_sound.js *
            });
            
        var check_Mask = document.querySelector('input[id=setMask]');
            check_Mask.addEventListener('change', function (event) {
            
            var setMask = document.getElementById("maskView");
            var cyMask = document.getElementById("CyMask");
            var newMask = document.getElementById("newMask");
            var maskChange = document.getElementById("maskChange");
        
            if (check_Mask.checked) {
                setMask.style.display = 'inline';
                setMask.style.visibility = 'visible';
                cyMask.style.visibility = 'visible';
                newMask.style.visibility = 'visible';
                maskChange.style.visibility = 'visible';
            }
            else {
                setMask.style.display = 'none';
                setMask.style.visiblity = 'hidden';
                cyMask.style.visibility = 'hidden';
                newMask.style.visibility = 'hidden';
                maskChange.style.visibility = 'hidden';
            }
        
        });

            var scroll_checked = document.querySelector('input[id=CyScroll]');
            scroll_checked.addEventListener('change', function (event) {
            play_beep(1);    // play_sound.js *
            scroll_check = document.getElementById("CyScroll").checked;
            resizeCanvas()   // graphics.js *
            
            //ctx.fillRect(0, 0, canvasWidth, canvasHeight);
            });

            baseline_checked = document.querySelector('input[id=CyBaseline]');
            
            baseline_checked.addEventListener('change', function (event) {
            play_beep(1); // play_sound.js *
            baseline_check = document.getElementById("CyBaseline").checked;
            pyBaseline = document.getElementById("PyBaseline").checked;
            if (client != null) {
                client.sendData("CyKITv2:::setBaselineMode:::" + ((pyBaseline && baseline_check) ? 1 : 0));
                }
            });
            
        /*
        
        var gyro_check = document.querySelector('input[id=balanceGyro]');
            gyro_check.addEventListener('change', function (event) {
            balanceGyro = document.getElementById("balanceGyro").checked;
        
        if (balanceGyro == true) {
            //var update_gyro = setInterval( function() { balance_gyros(); }, 10);
        }
        else {
            if (update_gyro != null) {
                clearInterval(update_gyro);
                update_gyro = null;
            }
        }
        });
        
        balanceGyro = document.getElementById("balanceGyro").checked;
        if (balanceGyro == true) {
            var update_gyro = setInterval( function() { balance_gyros(); }, 200);
        }
        
        */
        
        var pyBaseline_checked = document.querySelector('input[id=PyBaseline]');
            pyBaseline_checked.addEventListener('change', function (event) {
            play_beep(1); // play_sound.js *
            baseline_check = document.getElementById("CyBaseline").checked;
            pyBaseline = document.getElementById("PyBaseline").checked;
            client.sendData("CyKITv2:::setBaselineMode:::" + ((pyBaseline && baseline_check) ? 1 : 0));
            });
        
        EEG_View = document.querySelector('input[id=enable-EEG-View]');
            EEG_View.addEventListener('change', function (event) {
            openTab("Calibration");
            
            });
        
        var Gyro_View = document.querySelector('input[id=enable-Gyro-View]');
            Gyro_View.addEventListener('change', function (event) {
            
            openTab("Calibration");
            
            });
                    
        var singleWave = document.querySelector('input[id=enable-singleWave]');
            singleWave.addEventListener('change', function (event) {
                play_beep(1); // play_sound.js *
            });
        
        var boldWave = document.querySelector('input[id=enable-boldWave]');
            boldWave.addEventListener('change', function (event) {
                play_beep(1); // play_sound.js *

                if (boldWave.checked == true) { 
                    line_size = "1.5";
                }
                else {
                    line_size = ".6";
                }
            });
            
        var all_checked = document.querySelector('input[id="e.ALL"]');
            all_checked.addEventListener('change', function (event) {
                all_check = document.getElementById("e.ALL").checked;
                play_beep(1); // play_sound.js *
                
                if (selected_model == null) { return; }
                    device_name = headset[selected_model].replace('epoc_plus','epoc');
                    for (arr_index in sensorNAME[device_name]) {
                        document.getElementById(("e." + sensorNAME[device_name][arr_index])).checked = all_check;
                    }
                
            });

        
        resizeCanvas();
        
        openTab("EEG");
       
       //  Set Theme from link:  CyKITv2.html?theme=3
       // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
       var link_theme = window.location.search.substring(1);
       var link_var = link_theme.split("?");
       console.log(link_var);
       
       if (link_var[0].includes("nosound")) {
            sound_disabled = true;
       }
       
       if (link_var[0].includes("theme")) {
            
            var init_theme = (parseInt(link_var[0].split("=")[1]) - 1);
            console.log(init_theme);
            console.log(themes[init_theme]);
            setTheme(themes[init_theme]);
       }
       else {
        setTheme(themes[0]);
       
       }
       

        // Level off and average Gyro sliders.
        function balance_gyros() { 
            return;
            if (current_tab != "Gyro") { return; }
            for (i = 4; i < 10; i++) {
                var gyroObj = document.getElementById('sliderID.' + (i-1));
                        
                if ((gyroObj.value) > 6) {
                    gyroObj.value = gyroObj.value - 5;
                    if (i == 4) { console.log(" - " + gyroObj.value); }
                }
                if ((gyroObj.value) < -6) {
                    if (i == 4) { console.log(" + " + gyroObj.value); }
                    gyroObj.value = 2+ gyroObj.value;
                    
                }
                
            }       
        }

        
                //  Socket Command Input.
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        client.onCommand  = function(text) {
            var cyStatus = document.getElementById("CyStatus");
            var cyDevice = document.getElementById("CyDevice");
            var cySerial = document.getElementById("CySerial");
            var cyKeyModel = document.getElementById("CyKeyModel");
            var cyHeadset = document.getElementById("CyHeadset");
            var cyPicture = document.getElementById("CyKIT-picture");

            var selectINSIGHT = document.getElementById("selectInsightSensor");
            var selectEPOC = document.getElementById("selectEpocSensor");
            
            var newCmd = text.split(":::");
            //console.log(text)
            if (newCmd[1] == "Connected") {
                cyStatus.innerHTML = "Connected.";
                
                if (current_theme == "cyScientific") {
                    cyPicture.style.backgroundImage = "url('./images/CyKITv2-bg-neutral.png')";
                }
                else {
                    cyPicture.style.backgroundImage = "url('./images/CyKITv2-bg-edge.png')";
                }
                client.sendData("CyKITv2:::setDataMode:::" + 1);
            }
                       
            if (newCmd[2] == "serial") {
                cySerial.innerHTML = newCmd[3];
            }

            if (newCmd[2] == "device") {
                cyDevice.innerHTML = newCmd[3];
                var settingsButton = document.getElementById("tab.3");
                if (cyDevice.innerHTML == "EPOC+") {
                    settingsButton.disabled = false;
                }
                else {
                    settingsButton.disabled = true;
                }
            }
            
            if (newCmd[1] == "Baseline") {
                baseline = newCmd[2].split(delimiter);
                //console.log(baseline);
            }
            
            if (newCmd[1] == "datamode") {
                data_mode = parseInt(newCmd[2]);
            }
            
            if (newCmd[1] == "Info") {
                if (newCmd[2] == "config") {
                    console.log("Config Flags: " + newCmd[3]);
                    if (newCmd[3].includes("nocounter")) {
                        no_counter = true;
                    }
                    else {
                        no_counter = false;
                    }
                    
                    if (newCmd[3].includes("bluetooth")) {
                        bluetooth = "bt";
                        formatType = 1;
                        console.log("Format Type = " + formatType);
                    }
                    else {
                        bluetooth = "";
                        formatType = 0;
                        console.log("Format Type = " + formatType);
                    }
                    
                    if (newCmd[3].includes("gyromode")) {
                        data_mode = 2;
                    }

                    if (newCmd[3].includes("eegmode")) {
                        data_mode = 1;
                    }

                    if (newCmd[3].includes("nobattery")) {
                        no_battery = true;
                    }
                    else {
                        no_battery = false;
                    }
                
                    if (newCmd[3].includes("filter")) {
                        var filter_enabled = true;
                    }
                    else {
                        var filter_enabled = false;
                    }
                    console.log("Data Mode = " + data_mode);
                
                    if (no_battery == true || no_counter == true) {
                        var BatteryLevel = document.getElementById("CyBattery");
                        BatteryLevel.innerHTML = "N/A";
                    }
                  client.sendData("CyKITv2:::setBaselineMode:::" + ((pyBaseline && baseline_check) ? 1 : 0));
                }
                
                if (newCmd[2] == "delimiter") {
                    if (!isNaN(parseInt(newCmd[3], 10))) {
                        delimiter =  String.fromCharCode(parseInt(newCmd[3]));
                    }
                }
                
                //  Key Detection.       
                // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                if (newCmd[2] == "keymodel") {

                    cyKeyModel.innerHTML = newCmd[3];
                    //if (selected_model == parseInt(newCmd[3])) { return; }
                    selected_model = parseInt(newCmd[3])
                    device_name = headset[selected_model].replace('epoc_plus','epoc');
                    
                    //  Epoc Detected.
                    // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                    if (selected_model == 2 || selected_model == 1) {
                        loadModel = "epoc"
                        document.getElementById("convertFormat").style.display = "none"; 
                        selectINSIGHT.style.visibility = 'hidden';
                        selectEPOC.style.visibility = 'visible';
                        update_sensorList('epoc');

                        create_quality(14, 'epoc');
                        resizeCanvas();
                        /*
                        var sensorOption = document.createElement("option");
                        var sensorList = document.getElementById("CySelect");
                        sensorOption.text = "All Sensors";
                        sensorList.add(sensorOption);
                        
                        for (i = 0; i < 17; i++) {
                            var sensorOption = document.createElement("option");
                            sensorOption.text = epocContacts[i];
                            sensorOption.value = i;
                            sensorList.add(sensorOption);
                        }
                        */
                    }
                    
                    //  Insight Detected.
                    // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
                    if (selected_model == 4 || selected_model == 3) {
                        loadModel = "insight";
                        changeFormat(3);
                        document.getElementById("convertFormat").style.display = "block"; 
                        selectINSIGHT.style.visibility = 'visible';
                        selectEPOC.style.visibility = 'hidden';                       
                        create_quality(5, 'insight');
                        resizeCanvas();
                        
                        var sensorOption = document.createElement("option");
                        var sensorList = document.getElementById("CySelect");
                        
                        sensorOption.text = "All Sensors";
                        sensorList.add(sensorOption);
                        
                        update_sensorList('insight');
                        
                        for (i = 0; i < 33; i++) {
                            var sensorOption = document.createElement("option");
                            sensorOption.text = i;
                            sensorOption.value = i;
                            sensorList.add(sensorOption);
                        }

                    }

                    // Epoc+ Detected.
                    if (selected_model == 6 || selected_model == 5 || selected_model == 7) {
                        loadModel = "epocPlus";
                        document.getElementById("convertFormat").style.display = "block"; 
                        selectINSIGHT.style.visibility = 'hidden';
                        selectEPOC.style.visibility = 'visible';
                        create_quality(14, 'epoc');
                        resizeCanvas();
                        update_sensorList('epoc');
                    }
                    
                    // Flex Detected.
                    if (selected_model == 8) {
                        loadModel = "Flex";
                    }
                    
                    var loadModel = headset[selected_model];
                    if (loadModel != null) { 
                        loadjscssfile("./model_" + loadModel + ".js","js");
                        verify_load(loadModel); 
                    }
                    cyHeadset.innerHTML = modelTypes[selected_model];
                
                }
            }
        }
    
    client.onData  = function(text) {
        
        if (scriptLoaded == null) { return; }
        
        contact = text.split(delimiter);
        if (no_counter == true) { contact.unshift("0",(data_mode == 2 ? "32" : "16")); }

        //  Run functions from dynamically loaded script. 
        // ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
        process_EEG_data();     
        //process_Gyro_data(); 
        
    }
});

