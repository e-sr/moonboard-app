# -*- coding:utf-8 -*-

import json
import pickle
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
    print("Read problems from 'problems.pkl'")
    PROBLEMS = pickle.load(open('problems.pkl', 'rb'))
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
    collection, index = table_contents(PROBLEMS)
    results = BaseDataTables(request, COLUMNS, collection).output_result()
    # return the results as a string for the datatable
    return json.dumps({"data":[{'id':k, **v} for k,v in PROBLEMS.items()]})

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


class BaseDataTables:
    def __init__(self, request, columns, collection):
        self.columns = columns

        self.collection = collection

        # values specified by the datatable for filtering, sorting, paging
        self.request_values = request.values

        # results from the db
        self.result_data = None

        # total in the table after filtering
        self.cardinality_filtered = 0

        # total in the table unfiltered
        self.cadinality = 0

        self.run_queries()

    def output_result(self):
        output = {}

        # output['sEcho'] = str(int(self.request_values['sEcho']))
        # output['iTotalRecords'] = str(self.cardinality)
        # output['iTotalDisplayRecords'] = str(self.cardinality_filtered)

        output['aaData'] = self.collection  # [self.collection[i] for i in range(10)]

        return output

    def run_queries(self):
        self.result_data = self.collection
        self.cardinality_filtered = len(self.result_data)
        self.cardinality = len(self.result_data)


###


if __name__ == '__main__':
    app.run()