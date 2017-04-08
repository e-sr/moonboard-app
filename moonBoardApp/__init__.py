# moonboard-app/__init__.py
from flask import Flask
from flask_socketio import SocketIO
from flask_jsglue import JSGlue
import eventlet
from pathlib import Path
eventlet.monkey_patch()

###############
###############
# GLOBALS

####################
app = Flask(__name__)
app.config.from_object('config')
socket = SocketIO(app)
jsglue = JSGlue(app)

APP_ROOT = Path(__file__).parent.relative_to(Path().absolute())
STATIC_FILE_PATH = APP_ROOT.joinpath('static')
from moonBoardApp import main
from moonBoardApp import assets
