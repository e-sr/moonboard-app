function toggle_fullscreen(e){
    console.log('toggle fullscreen');
    //
    if (!document.webkitFullscreenElement){
        document.documentElement.webkitRequestFullscreen();
    }else{
        document.webkitExitFullscreen();
    }
};

//////////===================================================

$(document).ready(function() {

var socket = io.connect('http://' + document.domain + ':' + location.port );

//selcect hold setup
$("#select-hold-setup").on('change',function( event ){
  $.post( "/_set_holds_setup", {holds_setup_k: $(this).val()});
});

//test leds
document.getElementById("led-test-btn").addEventListener("click", function(){
    document.getElementById("test-report").style.display = 'block';
    document.getElementById("led-test-btn").classList.add("disabled");
    socket.emit('_start_leds_test');
    return false;
});

socket.on('test_report', function(message) {
    console.log(message.progress);
    var bar = $("#test-bar");
    var text = $("#test-text");
    bar.style.width = message.progress + '%';
    bar.innerHTML = message.progress + '%';
    if(message.done){
        console.log('btn_enable');
        document.getElementById("led-test-btn").classList.remove("disabled");
        text.innerHTML = message.report;
    };
});




//document.getElementById("fullscreen-btn").addEventListener("click",toggle_fullscreen);

});
