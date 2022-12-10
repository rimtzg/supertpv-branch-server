from flask import Blueprint, jsonify, request, abort

from methods.api import Methods
from methods import Discounts
from methods import Sales
from methods import Config

from routes.sessions import app as sessions

PREFIX = 'api'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)
app.register_blueprint(sessions)

@app.route('/', methods=['GET'])
def api():
    return jsonify({'status' : 'ok'})

@app.route('/login', methods=['GET'])
def login():
    return jsonify(Methods().login())

@app.route('/sales', methods=['GET'])
def get_sales():
    return jsonify(Methods().get_sales())

@app.route('/returns', methods=['GET'])
def get_returns():
    return jsonify(Methods().get_returns())

@app.route('/returns', methods=['POST'])
def save_return():
    return jsonify(Methods().save_return())

@app.route('/deposits', methods=['GET'])
def get_deposits():
    return jsonify(Methods().get_deposits())

@app.route('/deposits', methods=['POST'])
def save_deposit():
    return jsonify(Methods().save_deposit())

@app.route('/incomes', methods=['GET'])
def get_incomes():
    return jsonify(Methods().get_incomes())

@app.route('/incomes', methods=['POST'])
def save_income():
    return jsonify(Methods().save_income())

@app.route('/payments', methods=['GET'])
def get_payments():
    return jsonify(Methods().get_payments())

@app.route('/payments', methods=['POST'])
def save_payment():
    return jsonify(Methods().save_payment())

#CARD PAYMENTS
@app.route('/card_payments', methods=['GET'])
def get_card_payments():
    return jsonify(Methods().get_card_payments())

@app.route('/card_payments', methods=['POST'])
def save_card_payment():
    return jsonify(Methods().save_card_payment())

#CASH WITHDRAWALS
@app.route('/cash_withdrawals', methods=['GET'])
def get_cash_withdrawals():
    return jsonify(Methods().get_cash_withdrawals())

@app.route('/cash_withdrawals', methods=['POST'])
def save_cash_withdrawal():
    return jsonify(Methods().save_cash_withdrawal())

#
@app.route('/sale', methods=['GET'])
def get_sale():
    return jsonify(Methods().get_sale())

@app.route('/sale', methods=['POST'])
def save_sale():
    return jsonify(Sales().save())

@app.route('/product', methods=['GET'])
def get_product():
    return jsonify(Methods().get_product())

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(Methods().get_products())

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(Methods().get_orders())

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(Config().get())

@app.route('/discounts/get', methods=['POST'])
def get_discounts():
    return jsonify(Discounts().get())




