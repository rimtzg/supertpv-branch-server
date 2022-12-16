from flask import Blueprint, jsonify, request, abort

from methods import Sales

PREFIX = 'sale'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def get_session():
    return jsonify(Sales().get())

@app.route('/', methods=['POST'])
def save_session():
    return jsonify(Sales().save())

@app.route('/list', methods=['GET'])
def sessions():
    return jsonify(Sales().list())