/*

   CyKIT
   CySocketClient.js   2018.Dec.26
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
   Written by Warren
  
   CyKITv2 CyWebSocket client for dispatching event-driven data to eeg.py
   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
*/

function CySocketClient(ip,port,query) {
    var _this = this;
    this.socket = '';
    this.uid = 0;
    this.sign = '';
    this.connect = function(myIP, myPORT) {
        if (this.socket != '' && this.socket.readyState != 3) { 
            return; 
        }
        this.socket = new WebSocket('ws://'+myIP+':'+myPORT+'/'+query);
        this.socket.onopen = function() {
            _this.onOpen();
        
        }
        this.socket.onmessage = function(event) {
            data = event.data;
            data = data.split("<split>");
            _this.uid = data[0];
            _this.sign = data[1];
            text = data[2];

            command = text.substring(0,10);
            if (command == "CyKITv2:::") {
                _this.onCommand(text);
                return;
            }
            
            if (text != 'SETUID') {  
               _this.onData(text);
            } else {
                _this.onRegist();
            }
        }        
        this.socket.onclose = function(event) { 
            if (this.socket == '') { return; }
            _this.onClose();
        }; 
    }
    this.onRegist = function() {

    }
    this.onClose = function() {

    }

    this.onOpen = function() {
        console.log('Socket Open');
    }

    this.onData = function(text) {

    }
    
    this.sendData = function (text) {
        if (this.socket == '') { return; }
        if (this.socket.readyState != 1) { return; }
        var data = this.uid+'<split>'+this.sign+'<split>'+text;
        
        this.socket.send(data);
    }
    
    this.close = function() {
        if (this.socket == '') { return; }
        this.socket.close();
    }
}
