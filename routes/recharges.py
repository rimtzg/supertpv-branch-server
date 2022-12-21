from flask import Blueprint, jsonify, request, abort

from methods import Recharges

PREFIX = 'recharge'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def get():
    return jsonify(Recharges().get())

@app.route('/', methods=['POST'])
def save():
    return jsonify(Recharges().save())

@app.route('/list', methods=['GET'])
def list():
    return jsonify(Recharges().list())

@app.route('/balance', methods=['GET'])
def balance():
    return jsonify(Recharges().balance())