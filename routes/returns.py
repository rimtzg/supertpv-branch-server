from flask import Blueprint, jsonify, request, abort

from methods import Returns

PREFIX = 'returns'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def get_return():
    return jsonify(Returns().get())

@app.route('/', methods=['POST'])
def save_return():
    return jsonify(Returns().save())

@app.route('/calculate', methods=['POST'])
def calculate_total():
    return jsonify(Returns().calculate_total())

@app.route('/list', methods=['GET'])
def list_returns():
    return jsonify(Returns().list())