from flask import Blueprint, jsonify, request, abort

from methods import Recharges

PREFIX = 'recharge'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def get_session():
    return jsonify(Recharges().get())

@app.route('/', methods=['POST'])
def save_session():
    return jsonify(Recharges().save())

@app.route('/list', methods=['GET'])
def sessions():
    return jsonify(Recharges().list())