from flask_assets import Bundle

bundles = {
    "home_js": Bundle(
        "frontend/jquery-3.2.1.min.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-3.3.7/js/bootstrap.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/DataTables/datatables.js",
        "frontend/myjs/home.js",
        output="js-generated/home.js"),

    "home_css": Bundle(
        "frontend/bootstrap-3.3.7/css/bootstrap.css",
        "frontend/bootstrap-select/dist/css/bootstrap-select.css",
        "frontend/DataTables/datatables.css",
        "frontend/jqbtk-0.2/jqbtk.min.css",
        "frontend/mycss/home.css",
        output="css-generated/home.css"),

    "setting_js": Bundle(
        "frontend/jquery-3.2.1.min.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-3.3.7/js/bootstrap.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/myjs/setting.js",
        output="js-generated/setting.js"),
    "utils_js": Bundle(
        "frontend/jquery-3.2.1.min.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-3.3.7/js/bootstrap.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/myjs/utils.js",
        output="js-generated/utils.js"),
    "audio_visualization_js": Bundle(
        "frontend/jquery-3.2.1.min.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-3.3.7/js/bootstrap.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/myjs/audio_visualization.js",
        output="js-generated/audio_visualization.js"),
    "custom_js": Bundle(
        "frontend/jquery-3.2.1.min.js",
        "frontend/socket.io-client-master/dist/socket.io.min.js",
        "frontend/bootstrap-3.3.7/js/bootstrap.js",
        "frontend/bootstrap-select/dist/js/bootstrap-select.js",
        "frontend/jqbtk-0.2/jqbtk.min.js",
        "frontend/myjs/custom.js",
        output="js-generated/custom.js"),
}
