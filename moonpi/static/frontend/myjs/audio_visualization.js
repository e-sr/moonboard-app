$(document).ready(function () {
    $("#start-audio-visualization-btn").on('click', function (event) {
        $.post("/_start_audio_visualization");
    });
});