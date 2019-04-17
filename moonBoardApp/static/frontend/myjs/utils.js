$(document).ready(function () {
    $("#sequence-test-btn").on('click', function (event) {
        $.post("/_sequence_test", {brightness: $(this).val()});
    });
    $("#matrix-calibration-btn").on('click', function (event) {
        $.post("/_matrix_calibration", {brightness: $(this).val()});
    });
    $("#bloom-effect-btn").on('click', function (event) {
        $.post("/_bloom_effect", {brightness: $(this).val()});
    });
    $("#matrix-rain-btn").on('click', function (event) {
        $.post("/_matrix_rain", {brightness: $(this).val()});
    });
    $("#matrix-rainbow-btn").on('click', function (event) {
        $.post("/_matrix_rainbow", {brightness: $(this).val()});
    });
    $("#mario-btn").on('click', function (event) {
        $.post("/_mario", {brightness: $(this).val()});
    });
    $("#clear-btn").on('click', function (event) {
        $.post("/_clear_wall");
    });
});