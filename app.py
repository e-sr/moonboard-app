# -*- coding:utf-8 -*-

import json
from get_moonboard_problems import update_problems
from drive_moonboard_LEDS import  init_moonboard, LED_DRIVER, PIXELS_DRIVER, test_leds, show_problem
from flask import Flask, request, render_template
from flask_jsglue import JSGlue




app = Flask(__name__)
jsglue = JSGlue(app)
app.debug = True

# GLOBALS
MOONBOARD_LEDS = init_moonboard(LED_DRIVER,PIXELS_DRIVER)

try:
    print("Read problems from 'problems.json'")
    PROBLEMS = json.load(open('problems.json', 'r+'))
except FileNotFoundError:
    print("File not found")
    PROBLEMS = {}
    print('Empty problems dict')
else:
    print("Problems founds: {}".format(len(PROBLEMS)))

SELECTED_PROBLEM_KEY = None
LED_ON = False

COLUMNS = ['name','grade','author']

@app.route('/')
def index():
    return render_template('index.html', columns = COLUMNS)

@app.route('/_get_problems')
def get_problems_data():
    data = []
    for k, v in PROBLEMS.items():
        d = {'id':k}
        d.update(v)
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
    #return json.dumps({})

###


def table_contents(problems):
    select = lambda r: [r[k] for k in COLUMNS]
    collection = []
    index = []
    for k, p in problems.items():
        index.append(k)
        collection.append(select(p))
    return collection, index

    def run_queries(self):
        self.result_data = self.collection
        self.cardinality_filtered = len(self.result_data)
        self.cardinality = len(self.result_data)


###


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)