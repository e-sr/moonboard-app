
function toggle_fullscreen(e){
    console.log('toggle fullscreen');
    //
var docElm = document.documentElement;
if (docElm.requestFullscreen) {
docElm.requestFullscreen();
}
else if (docElm.mozRequestFullScreen) {
docElm.mozRequestFullScreen();
}
else if (docElm.webkitRequestFullScreen) {
docElm.webkitRequestFullScreen();
}
else if (docElm.msRequestFullscreen) {
docElm.msRequestFullscreen();
}
};

function selected_hold_set() {
   console.log($("#hold_OS").is(':checked'));
   console.log($("#hold_A").is(':checked'));
   console.log($("#hold_B").is(':checked'));
};

function show_modal(){
console.log("show-board-modal");
document.getElementById('board-modal-img').src = document.getElementById('board-img').src;
document.getElementById('board-modal').modal();
return false
};

function centerModal() {
    $(this).css('display', 'block');
    var $dialog = $(this).find(".modal-dialog");
    var offset = ($(window).height() - $dialog.height()) / 2;
    // Center modal vertically in window
    $dialog.css("margin-top", offset);
}

//////////===================================================

$(document).ready(function() {

var socket = io.connect('http://' + document.domain + ':' + location.port );

 });

 document.getElementById("fullscreen-btn").addEventListener("click",toggle_fullscreen,false)

//====================================================//
//                      settings
//====================================================//

$("#select-hold-set :input").change(selected_hold_set);


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

document.getElementById("image-button").addEventListener("click",show_modal);


$('.modal').on('show.bs.modal', centerModal);
 //(window).on("resize", function () {
//    $('.modal:visible').each(centerModal);
//});

$('#toggle-led').change(function() {
    $.post("/_toggle_led_event", {
    toggle_led: $(this).prop('checked') } );
});




});