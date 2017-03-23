# -*- coding:utf-8 -*-

import json
from moonBoardApp import app, socket, eventlet
from flask import render_template, request

from get_moonboard_problems import PROBLEMS, HOLDS_SETS, update_problems
from drive_moonboard_LEDS import  MOONBOARD_LEDS, test_leds, show_problem


COLUMNS = ['name','grade','author']
SELECTED_PROBLEM_KEY = None

CURRENT_HOLD_SET= {'Hold Set B 2016',
                   'Hold Set A 2016',
                   'Original School Holds 2016'}

LED_ON = False


@app.route('/')
def index():
    return render_template('index.html', columns = COLUMNS)


@app.route('/settings/')
def settings():
    return render_template("settings.html")

@app.route('/_get_problems')
def get_problems_data():
    data = []
    hold_set_naming = {
        'Hold Set B 2016': 'B',
        'Hold Set A 2016':'A',
        'Original School Holds 2016':'SchoolHolds'
    }
    for k, v in PROBLEMS.items():
        d = {'id':k}
        d.update(v)
        d["hold_sets"] = [hold_set_naming[name] for name in sorted(d["hold_sets"])]
        data.append(d)

    return json.dumps({"data":data})

@app.route('/_select_problem', methods=['POST'])
def select_problem():
    problem_id = request.form['problem_id']
    SELECTED_PROBLEM_KEY = problem_id
    holds = PROBLEMS.get(SELECTED_PROBLEM_KEY, {}).get('holds', {})
    print(holds)

    return "OK"#json.dumps(PROBLEMS[SELECTED_PROBLEM_KEY])

@app.route('/_toggle_led_event',  methods=['POST'])
def toggle_led_event():
    toggle_led = request.form['toggle_led']
    if toggle_led=="true":
        LED_ON=True
        holds = PROBLEMS.get(SELECTED_PROBLEM_KEY,{}).get('holds',{})
        show_problem(MOONBOARD_LEDS, holds, brightness=200)
    else:
        LED_ON=False
        show_problem(MOONBOARD_LEDS, {}, brightness = 0)
    print(LED_ON)
    return "OK"

@socket.on('connect')
def test_connect():
    print('Client connected')
    socket.emit('my response', {'data': 'Connected'})

@socket.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socket.on('start_leds_test')
def leds_test():
    def log_func(d):
            socket.emit('test_report', d)
    eventlet.spawn(test_leds,0,log_func)

@socket.on('start_update')
def leds_test():
    def log_func(d):
            socket.emit('test_report', d)
    eventlet.spawn(test_leds,0,log_func)

#####################################
if __name__ == '__main__':
    socket.run(app)