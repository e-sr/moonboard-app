$(document).ready(function () {
    $("#sequence-test-btn").on('click', function (event) {
        $.post("/_sequence_test");
    });
    $("#matrix-calibration-btn").on('click', function (event) {
        $.post("/_matrix_calibration");
    });
    $("#bloom-effect-btn").on('click', function (event) {
        $.post("/_bloom_effect");
    });
    $("#matrix-rain-btn").on('click', function (event) {
        $.post("/_matrix_rain");
    });
    $("#matrix-rainbow-btn").on('click', function (event) {
        $.post("/_matrix_rainbow");
    });
    $("#mario-btn").on('click', function (event) {
        $.post("/_mario");
    });
    $("#twinkle-btn").on('click', function (event) {
        $.post("/_twinkle");
    });
    $("#pinwheel-btn").on('click', function (event) {
        $.post("/_pinwheel");
    });
    $("#clear-btn").on('click', function (event) {
        $.post("/_clear_wall");
    });
    $('#scroll-text').keyboard();
    $('#scroll-fps').keyboard({type: 'tel'});
    $('#scroll-text-btn').on('click', function (event) {
        $.post('/_scroll_text', {
            text: $('#scroll-text').val(),
            fps: $('#scroll-fps').val(),
        });
    });

});