import json
import os

from flask import Flask, jsonify

app = Flask(__name__)

json_data = []

def run_flask():
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'  # Suppress startup messages in stdout
    app.run()


def save_json(data):
    """
    Simple function to store json List data to memory
    :param data: JSON data to write to file
    :return: None
    """
    json_data.extend(data)



@app.route('/tweets')
def json_response():
    return jsonify(json_data)

