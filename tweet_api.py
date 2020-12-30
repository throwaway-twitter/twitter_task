import logging
import os

from flask import Flask, jsonify

app = Flask(__name__)

json_data = []

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def run_flask():
    """
    starts the Flask API server
    :return: None
    """
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'  # Suppress startup messages in stdout
    app.run(host='0.0.0.0')


def save_json(data):
    """
    Simple function to store json List data to memory
    :param data: JSON data to write to file
    :return: None
    """
    json_data.extend(data)


@app.route('/tweets')
def json_response():
    """
    sends stored JSON data for user
    :return: Serialised JSON data
    """
    return jsonify(json_data)

