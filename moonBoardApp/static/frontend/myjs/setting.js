$(document).ready(function() {

//selcect hold setup
$("#select-hold-setup").on('change',function( event ){
  $.post( "/_set_holds_setup", {holds_setup_k: $(this).val()});
});


$("#select-brightness").on('change',function( event ){
  $.post( "/_set_led_brightness", {brightness: $(this).val()});
});
});
