from flask import Blueprint, jsonify, request, abort

from methods.api import Methods
PREFIX = 'api'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def api():
    return jsonify({'status' : 'ok'})

@app.route('/login', methods=['GET'])
def login():
    return jsonify(Methods().login())

@app.route('/sessions', methods=['GET'])
def sessions():
    return jsonify(Methods().sessions())

@app.route('/session/new', methods=['GET'])
def new_session():
    return jsonify(Methods().new_session())

@app.route('/sales', methods=['GET'])
def get_sales():
    return jsonify(Methods().get_sales())

@app.route('/returns', methods=['GET'])
def get_returns():
    return jsonify(Methods().get_returns())

@app.route('/deposits', methods=['GET'])
def get_deposits():
    return jsonify(Methods().get_deposits())

@app.route('/incomes', methods=['GET'])
def get_incomes():
    return jsonify(Methods().get_incomes())

@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(Methods().get_payments())

@app.route('/card_payments', methods=['GET'])
def get_card_payments():
    return jsonify(Methods().get_card_payments())



@app.route('/product', methods=['GET'])
def get_product():
    return jsonify(Methods().get_product())