from flask_assets import Bundle, Environment
from moonBoardApp import app

bundles = {
    "home_js": Bundle(
        "frontend/DataTables/datatables.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/myjs/home.js",
        output="js/home.js"),

    "home_css": Bundle(
        "frontend/DataTables/datatables.css",
        "frontend/bootstrap-select/dist/css/bootstrap-select.css",
        output="css/home.css"),

    "setting_js": Bundle(
        "frontend/DataTables/datatables.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/myjs/setting.js",
        output="js/setting.js"),
}

assets = Environment(app)
assets.register(bundles)