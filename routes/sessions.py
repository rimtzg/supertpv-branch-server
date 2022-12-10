from flask import Blueprint, jsonify, request, abort

from methods import Sessions

PREFIX = 'session'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def get_session():
    return jsonify(Sessions().get())

@app.route('/new', methods=['GET'])
def new_session():
    return jsonify(Sessions().new())

@app.route('/save', methods=['POST'])
def save_session():
    return jsonify(Sessions().save())

@app.route('/close', methods=['GET'])
def close_session():
    return jsonify(Sessions().close())

@app.route('/list', methods=['GET'])
def sessions():
    return jsonify(Sessions().list())