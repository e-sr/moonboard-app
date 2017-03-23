# moonboard-app/__init__.py

import json
from get_moonboard_problems import update_problems
from drive_moonboard_LEDS import  init_moonboard, LED_DRIVER, test_leds, show_problem
from flask import Flask, request, render_template
from flask.ext.socketio import SocketIO, emit
from flask_assets import Bundle, Environment
#from flask_jsglue import JSGlue
import logging
import eventlet
eventlet.monkey_patch()

###############
###############
# GLOBALS
MOONBOARD_LEDS = init_moonboard(LED_DRIVER,PIXELS_DRIVER)

try:
    print("Read problems from 'problems.json'")
    PROBLEMS = json.load(open('problems.json', 'r+'))
except IOError:
    print("File not found")
    PROBLEMS = {}
    print('Empty problems dict')
else:
    print("Problems founds: {}".format(len(PROBLEMS)))

HOLDS_SETS = {'Hold Set B 2016','Hold Set A 2016','Original School Holds 2016'}
CURRENT_HOLD_SET= {'Hold Set B 2016',
                   'Hold Set A 2016',
                   'Original School Holds 2016'}

SELECTED_PROBLEM_KEY = None
LED_ON = False

COLUMNS = ['name','grade','author']


####################
####################

app = Flask(__name__)
app.config.from_object('config')
socket = SocketIO(app)
assets = Environment(app)

assets.register(bundles)

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
