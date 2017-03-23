# moonboard-app/__init__.py

from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
from flask_jsglue import JSGlue
import eventlet
eventlet.monkey_patch()

###############
###############
# GLOBALS

####################
app = Flask(__name__)
app.config.from_object('config')
socket = SocketIO(app)



from moonBoardApp import main
from moonBoardApp import assets