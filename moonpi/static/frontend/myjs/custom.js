$(document).ready(function () {
    let keyboard_config = {
        layout: [
            [
                ['a', 'A'],
                ['b', 'B'],
                ['c', 'C'],
                ['d', 'D'],
                ['e', 'E'],
                ['f', 'F'],
                ['g', 'G'],
                ['h', 'H'],
                ['i', 'I'],
                ['j', 'J'],
                ['k', 'K'],
                ['del', 'del']
            ],
            [
                ['1', '1'],
                ['2', '2'],
                ['3', '3'],
                ['4', '4'],
                ['5', '5'],
                ['6', '6'],
                ['7', '7'],
                ['8', '8'],
                ['9', '9'],
                ['0', '0']
            ],
            [[',', ',']]
        ]
    };
    $('#initialHolds').keyboard(keyboard_config);
    $('#intermediateHolds').keyboard(keyboard_config);
    $('#finishHolds').keyboard(keyboard_config);
    $('#custom-problem-btn').on('click', function (event) {
        $.post('/_set_custom_problem', {
            initialHolds: $('#initialHolds').val(),
            intermediateHolds: $('#intermediateHolds').val(),
            finishHolds: $('#finishHolds').val()
        });
    });
    $('#clear-btn').on('click', function (event) {
        $.post('/_clear_wall');
    });
});