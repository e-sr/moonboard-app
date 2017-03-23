from flask_assets import Bundle, Environment
from moonBoardApp import app

bundles = {
    'home_js': Bundle(
        "frontend/DataTables/datatables.js",
        'frontend/myjs/home.js',
        output='js/home.js'),

    'home_css': Bundle(
        'frontend/DataTables/datatables.css',
        output='css/home.css')
}

assets = Environment(app)
assets.register(bundles)