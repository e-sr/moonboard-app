from flask_assets import Bundle, Environment
from moonBoardApp import app

bundles = {
    "home_js": Bundle(
        "frontend/jquery-3.2.1.min.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-3.3.7/js/bootstrap.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/DataTables/datatables.js",
        "frontend/myjs/home.js",
        output="js/home.js"),

    "home_css": Bundle(
        "frontend/bootstrap-3.3.7/css/bootstrap.css",
        "frontend/bootstrap-select/dist/css/bootstrap-select.css",
        "frontend/DataTables/datatables.css",
        "frontend/mycss/home.css",
        output="css/home.css"),

    "setting_js": Bundle(
        "frontend/jquery-3.2.1.min.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-3.3.7/js/bootstrap.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/myjs/setting.js",
        output="js/setting.js"),
}

assets = Environment(app)
assets.register(bundles)