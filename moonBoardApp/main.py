# -*- coding:utf-8 -*-

import json

from moonBoardApp import app, socket, eventlet, jsglue, APP_ROOT,STATIC_FILE_PATH
from flask import render_template, request,redirect,url_for

from moonboard_problems import HOLDS_CONF, site_update_problems, load_problems
from draw_problem import draw_Problem
from drive_moonboard_LEDS import  MOONBOARD_LEDS, test_leds, show_problem

##GLOBALS
PROBLEMS_FILE_PATH = str(APP_ROOT.joinpath('problems.json'))
PROBLEM_IMAGE_PATH = str(STATIC_FILE_PATH.joinpath("img").joinpath('current_problem.png'))

PROBLEMS = load_problems(PROBLEMS_FILE_PATH)

# A+B+OS 2016
CURRENT_HOLD_SETUP_KEY= 1
SELECTED_PROBLEM_KEY = None
LED_BRIGHTNESS = 100

#draw empty problem
draw_Problem({'holds_setup':HOLDS_CONF['setup'][CURRENT_HOLD_SETUP_KEY]}, PROBLEM_IMAGE_PATH)

#views

@app.route('/')
def index():
    return redirect(url_for('problems_table'))

@app.route('/problems_table')
def problems_table():
    columns = ['name', 'grade', 'author']
    grades_list =sorted(list({v['grade'] for k, v in PROBLEMS.items()}))
    return render_template('problems_table.html', columns = columns, grades=grades_list)

@app.route('/settings')
def settings():
    setup = {k:{ 'name':", ".join(list(v)), 'selected': k == CURRENT_HOLD_SETUP_KEY} \
                      for k,v in HOLDS_CONF["setup"].items()}
    return render_template("settings.html", holds_setup= setup)

@app.route('/_get_problems')
def get_problems_data():
    data = []
    current_hold_setup = HOLDS_CONF["setup"][CURRENT_HOLD_SETUP_KEY]
    for k, v in PROBLEMS.items():
        if set(v["holds_setup"]).issubset(current_hold_setup):
            d = {'id':k}
            d.update(v)
            d["holds_setup_short"] = [HOLDS_CONF["configurations"].get(name,{}).get('shortName') for name in sorted(d["holds_setup"])]
            data.append(d)
    return json.dumps({"data":data})

@app.route('/_select_problem', methods=['POST'])
def select_problem():
    global SELECTED_PROBLEM_KEY
    problem_id = request.form['problem_id']
    if problem_id=="":
        print(" No selected problem.")
        SELECTED_PROBLEM_KEY = None
        draw_Problem({'holds_setup': HOLDS_CONF['setup'][CURRENT_HOLD_SETUP_KEY]}, PROBLEM_IMAGE_PATH)
        show_problem(MOONBOARD_LEDS, {}, brightness=0)
    else:
        print("Selected problem ID: {}".format(problem_id))
        SELECTED_PROBLEM_KEY = problem_id
        holds = PROBLEMS.get(SELECTED_PROBLEM_KEY, {}).get('holds', {})
        draw_Problem(PROBLEMS.get(SELECTED_PROBLEM_KEY, {}), PROBLEM_IMAGE_PATH )
        show_problem(MOONBOARD_LEDS, holds, brightness=LED_BRIGHTNESS)
    return "OK"

@app.route('/_set_holds_setup', methods=['POST'])
def _set_hold_combination():
    global CURRENT_HOLD_SETUP_KEY
    CURRENT_HOLD_SETUP_KEY = int(request.form.get('holds_setup_k'))
    print CURRENT_HOLD_SETUP_KEY
    #current_holds = list(HOLDS_CONF['combinations'][CURRENT_HOLDS_SETUP_KEY])
    return "OK"

@app.route('/_set_led_brightness',  methods=['POST'])
def _set_led_brightness():
    global LED_BRIGHTNESS
    LED_BRIGHTNESS = int(request.form.get('hold_comb_k'))
    return "OK"

@socket.on('connect')
def test_connect():
    socket.emit('my response', {'data': 'Connected'})

@socket.on('disconnect')
def test_disconnect():
    #Todo: turn led OFF
    print('Client disconnected, Turn led OFF')

@socket.on('_start_leds_test')
def leds_test():
    def log_func(d):
            socket.emit('test_report', d)
    eventlet.spawn(test_leds,0,log_func)

@socket.on('_update_problems')
def leds_test():
    def log_func(d):
            socket.emit('update_report', d)
    eventlet.spawn(site_update_problems,0,log_func)

#####################################
if __name__ == '__main__':
    socket.run(app)