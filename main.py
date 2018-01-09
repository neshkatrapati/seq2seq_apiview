from bottle import route, run, template, static_file, request, post
import sys
import os
import json
import datetime
from predictions import *


MODELS_FILE = './models.json'
HELP_FILE = './help.json'

def load_models():
    return json.loads(open(MODELS_FILE).read())

MODELS = load_models()


def predict(model_name, input_text):
    model_mode = MODELS['models'][model_name]['mode']
    hierarchial = False
    if model_mode == 'single':
        input_text = input_text[0]
    elif model_mode == 'join':
        input_text = ' <eos> '.join(input_text)
    elif model_mode == "hierarchial":
        hierarchial = True
    print(input_text)
    output = predict_with_checkpoint(MODELS['models'][model_name]['path'], input_text, hierarchial)
    return ' '.join(output)

@route('/json')
def index_json():
    return MODELS


@route('/help/json')
def help_json():
    return json.loads(open(HELP_FILE).read())

@route('/', method='GET')
@route('/', method='POST')
def index():
    output_text = "Output text"
    selected_model = list(sorted(MODELS['models'].keys()))[0]
    input_text = "Enter Input"
    join_output = ""
    json_dict = {}

    if 'model' in request.query:
        selected_model = request.query['model']

    if 'input' in request.query:
        input_text = request.query['input']

    if request.method == 'POST':
        model_choice = request.forms.get('model_list')
        text_input = request.forms.get('input_text')
        join_output = request.forms.get('join_output')
        print(model_choice, text_input, join_output)
        selected_model = model_choice

        input_text = text_input.strip()
        text_input = text_input.strip().split('\n')
        json_dict['input'] = text_input
        output_text = predict(model_choice, text_input)
        if join_output == 'on':
            input_text += '\n' + output_text
            join_output = 'checked'
        #join_output = 'checked' if join_output == True else ""
        print(output_text)

    return template('index', models = MODELS['models'],
                    input_text = input_text,
                    output_text=output_text,
                    selected_model=selected_model,
                    join_output = join_output,
                    json_text = json.dumps(json_dict),
                    source_url = request.url)


@route('/i/<model>/json', method='POST')
def json_output(model):
    params = request.json
    params['model'] = model
    params['output'] = predict(model, params['input'])
    return params

@route('/static/<filename:path>')
def server_static(filename):
    print(filename)
    return static_file(filename, root='static/')

run(host='0.0.0.0', port=8888)