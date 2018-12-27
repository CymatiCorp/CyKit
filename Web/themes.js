/*

   CyKIT
   themes.js   2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   Themes for CyKIT.html interface
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
 */
function setTheme(change_theme) {
    
    current_theme = change_theme;
    if (current_theme != "cyBlue") {
        var changeClass = document.getElementById("taskBar");
            changeClass.classList.remove("w3-bar");
            changeClass.classList.remove("w3-black");
        var changeClass = document.getElementById("cyConnect");
            changeClass.classList.remove("w3-hover-black");
            changeClass.classList.remove("w3-hover-blue");
            changeClass.classList.add("w3-gray");
        var changeClass = document.getElementById("cyDisconnect");
            changeClass.classList.remove("w3-hover-black");
            changeClass.classList.remove("w3-hover-red");
            changeClass.classList.add("w3-gray");
        
            color_theme = 4;
    }
    
    if (current_theme == "cyBlue") {
        document.getElementById("enable-EEG-View").checked = false;
        document.getElementById("enable-Gyro-View").checked = false;
        
        var changeClass = document.getElementById("taskBar");
            changeClass.classList.add("w3-bar");
            changeClass.classList.add("w3-black");
        var changeClass = document.getElementById("cyConnect");
            //changeClass.classList.add("w3-bar-item");
            changeClass.classList.remove("w3-gray");        
            changeClass.classList.remove("w3-hover-white");
            changeClass.classList.add("w3-black");
            changeClass.classList.add("w3-hover-blue");
        
        var changeClass = document.getElementById("cyDisconnect");
            //changeClass.classList.add("w3-bar-item");
            changeClass.classList.remove("w3-gray");
            changeClass.classList.remove("w3-white");
            changeClass.classList.add("w3-black");
            changeClass.classList.add("w3-hover-red");
            
            
            color_theme = 0;
    }

    if (current_theme == "cyGray") {
        var changeClass = document.getElementById("taskBar");
            changeClass.classList.add("w3-black");    
        
        var changeClass = document.getElementById("cyConnect");
            //changeClass.classList.add("w3-bar-item");
            changeClass.classList.remove("w3-gray");        
            changeClass.classList.add("w3-black");
            changeClass.classList.add("w3-hover-white");
        
        var changeClass = document.getElementById("cyDisconnect");
            //changeClass.classList.add("w3-bar-item");
            changeClass.classList.remove("w3-gray");
            changeClass.classList.add("w3-black");
            changeClass.classList.add("w3-hover-white");
            
            color_theme = 3;
    }
    
    if (current_theme != "cyBlue") {
        var color_buttons = document.getElementsByClassName("w3-button"); 
        //while (color_buttons.length) {
        for (var i = 0; i < color_buttons.length; i++) {
            color_buttons[i].classList.remove("w3-hover-blue");
            color_buttons[i].classList.add("w3-hover-gray");
        }
    }
    else {
        var color_buttons = document.getElementsByClassName("w3-button"); 
        for (var i = 0; i < color_buttons.length; i++) {
            color_buttons[i].classList.add("w3-hover-blue");
            color_buttons[i].classList.remove("w3-hover-gray");
        }
    }
    
    
    var cssFile = "./Themes/" + change_theme  + ".css";
    var oldLink = document.getElementsByTagName("link").item(1);

    var newLink = oldLink;
        newLink.setAttribute("href", cssFile);
    document.getElementsByTagName("head").item(0).replaceChild(newLink, oldLink);
    
    if (current_tab == null) { current_tab = "EEG"; }
    openTab(current_tab);
    setTimeout(function() { resizeCanvas() }, 100);
    
    if (typeof eegData == 'undefined' || selected_model == 0) { return; }
    for (var i = 0; i < 14; i++) {
        eegData[i].style.backgroundColor = color_palette[(color_theme == 4 ? 3 : color_theme)][i];
    }

}
