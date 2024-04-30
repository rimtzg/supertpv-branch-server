from flask import Blueprint, jsonify, request, abort

from methods import CashWithdrawals

PREFIX = 'cash_withdrawals'

app = Blueprint(PREFIX, __name__, url_prefix = '/'+PREFIX)

@app.route('/', methods=['GET'])
def get_cash_withdrawals():
    return jsonify(CashWithdrawals().get())

@app.route('/', methods=['POST'])
def save_cash_withdrawals():
    return jsonify(CashWithdrawals().save())

@app.route('/list', methods=['GET'])
def list_cash_withdrawals():
    return jsonify(CashWithdrawals().list())