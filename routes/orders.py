from flask import Blueprint, jsonify, request, abort

from methods import Orders

PREFIX = 'orders'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def get():
    return jsonify(Orders().get())

@app.route('/', methods=['POST'])
def save():
    return jsonify(Orders().save())

@app.route('/list', methods=['GET'])
def list():
    return jsonify(Orders().list())