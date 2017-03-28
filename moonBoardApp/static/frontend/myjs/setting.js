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

$("#select-hold-setup").on('change',function( event ){
  $.post( "/_set_holds_setup", {holds_setup_k: $(this).val()});
});

document.getElementById("led-test-btn").addEventListener("click", function(){
    document.getElementById("test-report").style.display = 'block';
    document.getElementById("led-test-btn").classList.add("disabled");
    socket.emit('start_leds_test');
    return false;
});

socket.on('test_report', function(message) {
console.log(message);
var bar = document.getElementById("test-bar");
var text = document.getElementById("test-text");
    bar.style.width = message.progress + '%';
    bar.innerHTML = message.progress * 1 + '%';
    text.innerHTML = message.report;
if(message.done){
console.log('btn_enable');
document.getElementById("led-test-btn").classList.remove("disabled");};
});

document.getElementById("led-test-btn").addEventListener("click", function(){
    document.getElementById("test-report").style.display = 'block';
    document.getElementById("led-test-btn").classList.add("disabled");
    socket.emit('start_leds_test');
    return false;
});

socket.on('test_report', function(message) {
console.log(message);
var bar = document.getElementById("test-bar");
var text = document.getElementById("test-text");
    bar.style.width = message.progress + '%';
    bar.innerHTML = message.progress * 1 + '%';
    text.innerHTML = message.report;
if(message.done){
console.log('btn_enable');
document.getElementById("led-test-btn").classList.remove("disabled");};
});

$('#toggle-led').change(function() {
    $.post("/_toggle_led_event", {
    toggle_led: $(this).prop('checked') } );
});

document.getElementById("fullscreen-btn").addEventListener("click",toggle_fullscreen);

});