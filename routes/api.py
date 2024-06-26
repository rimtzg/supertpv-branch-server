from flask import Blueprint, jsonify, request, abort

from methods.api import Methods
from methods import Discounts
from methods import Sales
from methods import Config
from methods import CashWithdrawals

from routes.sessions import app as sessions
from routes.sales import app as sales
from routes.recharges import app as recharges
from routes.returns import app as returns
from routes.orders import app as orders
from routes.cash_withdrawals import app as cash_withdrawals

PREFIX = 'api'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)
app.register_blueprint(sessions)
app.register_blueprint(sales)
app.register_blueprint(recharges)
app.register_blueprint(returns)
app.register_blueprint(orders)
app.register_blueprint(cash_withdrawals)

@app.route('/', methods=['GET'])
def api():
    return jsonify({'status' : 'ok'})

@app.route('/login', methods=['GET'])
def login():
    return jsonify(Methods().login())

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

@app.route('/product', methods=['GET'])
def get_product():
    return jsonify(Methods().get_product())

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(Methods().get_products())

@app.route('/config', methods=['GET'])
def get_config():
    return jsonify(Config().get())

@app.route('/discounts/get', methods=['POST'])
def calculate_discounts():
    return jsonify(Discounts().calculate_discounts())


#CASH WHITDRAWALS
@app.route('/cash_withdrawals', methods=['GET'])
def get_cash_withdrawals_bak():
    return jsonify(CashWithdrawals().list())

@app.route('/cash_withdrawals', methods=['POST'])
def save_cash_withdrawals():
    return jsonify(CashWithdrawals().save())