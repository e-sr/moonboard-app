# -*- coding: utf-8 -*-
# moonboard-app/__init__.py

from moonboard_problems import HOLDS_CONF, _new_site_problems_ids_and_author, load_problems, get_setups
from draw_problem import draw_Problem,background_image_path
from drive_moonboard_LEDS import init_pixels, test_leds, show_problem, clear_problem
from  assets import bundles

from flask import Flask,request,redirect,render_template,url_for
from flask_socketio import SocketIO
from flask_assets import Environment
#from flask_jsglue import JSGlue
import eventlet
eventlet.monkey_patch()

import json
import sched
from pathlib import Path
from PIL.ImageColor import colormap,getrgb

###############
###############
# GLOBALS
#paths
APP_ROOT = Path(__file__).parent.relative_to(Path().absolute())
STATIC_FILE_PATH = APP_ROOT.joinpath('static')
IMAGE_FOLDER_PATH  = STATIC_FILE_PATH.joinpath("img")
PROBLEMS_DIR_PATH = APP_ROOT.joinpath('problems')
PROBLEM_IMAGE_PATH = IMAGE_FOLDER_PATH.joinpath('current_problem.png')
#problems

LED_BRIGHTNESS = 100
HOLD_COLORS = {
    'SH': getrgb(colormap["blueviolet"]),
    'IH': getrgb(colormap["darkgreen"]),
    'FH': getrgb(colormap["red"])
}

#init led hardware and turn led off
MOONBOARD_PIXELS = init_pixels(type='raspberry')

CURRENT_HOLD_SETUP_KEY= 1 #A+B+OS 2016

def init_problems_var():
    global SELECTED_PROBLEM_KEY, PROBLEMS
    PROBLEMS = load_problems(PROBLEMS_DIR_PATH)

    SELECTED_PROBLEM_KEY = None
    #turn off leds
    clear_problem(MOONBOARD_PIXELS)
    #draw empty problem
    draw_Problem({},
                 background_image_path(IMAGE_FOLDER_PATH, CURRENT_HOLD_SETUP_KEY),
                 PROBLEM_IMAGE_PATH,
                 HOLD_COLORS)

    print("Number of problems founds: {}.".format(len(PROBLEMS)))
    print("Setups founds:")
    print get_setups(PROBLEMS)

####################
app = Flask(__name__)
app.debug=True
socket = SocketIO(app)
assets = Environment(app)
assets.register(bundles)
#jsglue = JSGlue(app)

@app.route('/')
def index():
    return redirect(url_for('problems_table'))

@app.route('/problems_table')
def problems_table():
    init_problems_var()
    columns = ['name', 'grade', 'author']
    grades_list =sorted(list({v['grade'] for k, v in PROBLEMS.items()}))
    return render_template('problems_table.html', columns = columns, grades=grades_list)

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
        draw_Problem({},
                     background_image_path(IMAGE_FOLDER_PATH, CURRENT_HOLD_SETUP_KEY),
                     PROBLEM_IMAGE_PATH,
                     HOLD_COLORS)
        clear_problem(MOONBOARD_PIXELS)
    else:
        print("Selected problem ID: {}".format(problem_id))
        SELECTED_PROBLEM_KEY = problem_id
        holds = PROBLEMS.get(SELECTED_PROBLEM_KEY, {}).get('holds', {})
        draw_Problem(PROBLEMS.get(SELECTED_PROBLEM_KEY, {}),
                     background_image_path(IMAGE_FOLDER_PATH, CURRENT_HOLD_SETUP_KEY),
                     PROBLEM_IMAGE_PATH,
                     HOLD_COLORS)
        show_problem(MOONBOARD_PIXELS, holds, HOLD_COLORS, brightness=LED_BRIGHTNESS)
    return "OK"

############
#settings
@app.route('/settings')
def settings():
    clear_problem(MOONBOARD_PIXELS)
    setup = {k:{ 'name':", ".join(list(v)), 'selected': k == CURRENT_HOLD_SETUP_KEY} \
                      for k,v in HOLDS_CONF["setup"].items()}
    return render_template("settings.html", holds_setup= setup)

@socket.on('connect')
def test_connect():
    socket.emit('my response', {'data': 'Connected'})
    print("Client connected")

@socket.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/_set_holds_setup', methods=['POST'])
def _set_hold_combination():
    global CURRENT_HOLD_SETUP_KEY
    CURRENT_HOLD_SETUP_KEY = int(request.form.get('holds_setup_k'))
    print  "C   hange hold setup to {}:{}.".format(CURRENT_HOLD_SETUP_KEY,HOLDS_CONF['setup'][CURRENT_HOLD_SETUP_KEY])
    return "OK"

@app.route('/_set_led_brightness',  methods=['POST'])
def _set_led_brightness():
    global LED_BRIGHTNESS
    LED_BRIGHTNESS = int(request.form.get('brightness'))
    return "OK"

@socket.on('_start_leds_test')
def leds_test():
    print "start test"
    def log_func(d):
            socket.emit('test_report', d)
            print d
    eventlet.spawn(test_leds, MOONBOARD_PIXELS, log_func= log_func, sleep_func = eventlet.sleep, delay = 10.0)

@socket.on('_update_problems')
def leds_test():
    def log_func(d):
            socket.emit('update_report', d)
    #eventlet.spawn(,0,log_func)


