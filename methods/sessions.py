import logging
from datetime import datetime

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from driver import mongo

class Methods():
    def new(self):
        data = request.args

        if(not data.get('cashier') ):
            abort(403)

        cashier = mongo['cashiers'].find_one({ '_id' : ObjectId(data['cashier']) })

        query = {
            '_id' : ObjectId(),
            'cashier_id' : cashier['_id'],
            'cashier_name' : cashier['name']
        }

        data = {
            'start_date' : datetime.utcnow(),
            'initial_money' : 0
        }

        session = mongo['sessions'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return session

    def save(self):
        args = request.args
        data = request.json

        if(not args.get('session')):
            abort(403)

        _id = ObjectId(args['session'])

        query = {
            '_id' : _id
        }

        session = mongo['sessions'].find_one_and_update(query, {"$set": data}, return_document=ReturnDocument.AFTER)

        return session

    def get(self):
        args = request.args

        if(not args.get('session')):
            abort(403)

        _id = ObjectId(args['session'])

        query = {
            '_id' : _id
        }

        session = mongo['sessions'].find_one( query )

        session = self.build_session(session)

        return session

    def close(self):
        args = request.args

        if(not args.get('session')):
            abort(403)

        _id = ObjectId(args['session'])

        query = {
            '_id' : _id
        }

        initial_money = 0

        session = mongo['sessions'].find_one(query)

        session = self.build_session(session)

        data = {
            'initial_money' :           session['initial_money'],
            'total_sales' :             session['total_sales'],
            'num_of_sales' :            session['num_of_sales'],
            'total_incomes' :           session['total_incomes'],
            'total_payments' :          session['total_payments'],
            'total_deposits' :          session['total_deposits'],
            'total_returns' :           session['total_returns'],
            'total_card_payments' :     session['total_card_payments'],
            'total_cash_withdrawals' :  session['total_cash_withdrawals'],
            'difference' :              session['difference'],
            'end_date' :                datetime.utcnow(),
            'closed' :                  True
        }

        mongo['sessions'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        return session

    def list(self):
        data = request.args

        if(not data.get('cashier') ):
            abort(403)

        query = {
            'cashier_id' : ObjectId(data['cashier']),
        }

        sessions = list(mongo['sessions'].find( query ).limit(10).sort([("start_date", -1)]))

        for session in sessions:
            session = self.build_session(session)

        return sessions

    def build_session(self, session):
        sales = list(mongo['sales'].find({'session' : session['_id']}))
        num_of_sales = len(sales)

        payments = list(mongo['payments'].find({'session' : session['_id']}))
            
        for payment in payments:
            if(payment.get('razon')):
                payment['reason'] = payment['razon']

        incomes = list(mongo['incomes'].find({'session' : session['_id']}))

        for income in incomes:
            if(income.get('razon')):
                income['reason'] = income['razon']

        deposits = list(mongo['deposits'].find({'session' : session['_id']}))
        returns = list(mongo['returns'].find({'session' : session['_id']}))
        card_payments = list(mongo['card_payments'].find({'session' : session['_id']}))
        cash_withdrawals = list(mongo['cash_withdrawals'].find({'session' : session['_id']}))

        session['sales'] = sales
        session['payments'] = payments
        session['incomes'] = incomes
        session['deposits'] = deposits
        session['returns'] = returns
        session['card_payments'] = card_payments
        session['cash_withdrawals'] = cash_withdrawals

        session['initial_money'] = session['initial_money']
        session['total_sales'] = self.get_total_sales(sales)
        session['num_of_sales'] = len(sales)
        session['total_incomes'] = self.get_total_incomes(incomes)
        session['total_payments'] = self.get_total_payments(payments)
        session['total_deposits'] = self.get_total_deposits(deposits)
        session['total_returns'] = self.get_total_returns(returns)
        session['total_card_payments'] = self.get_total_card_payments(card_payments)
        session['total_cash_withdrawals'] = self.get_total_cash_withdrawals(cash_withdrawals)
        session['difference'] = self.calculate_difference(session)
        session['end_date'] = session['end_date'] if session.get('end_date') else datetime.utcnow()
        session['closed'] = session['closed'] if session.get('closed') else False

        return session

    def get_total_sales(self, sales):
        total_sales = 0

        for sale in sales:
            if not(sale.get('canceled') and sale['canceled']):
                total_sales += sale['total']

        return total_sales

    def get_total_incomes(self, incomes):
        total_incomes = 0
        for income in incomes:
            total_incomes += income['amount']

        return total_incomes

    def get_total_payments(self, payments):
        total_payments = 0
        for payment in payments:
            total_payments += payment['amount']

        return total_payments

    def get_total_deposits(self, deposits):
        total_deposits = 0
        for deposit in deposits:
            total_deposits += deposit['total']

        return total_deposits

    def get_total_returns(self, returns):
        total_returns = 0
        for retur in returns:
            total_returns += retur['total']

        return total_returns

    def get_total_card_payments(self, card_payments):
        total_card_payments = 0
        for card_payment in card_payments:
            if(card_payment.get('amount')):
                total_card_payments += card_payment['amount']

        return total_card_payments

    def get_total_cash_withdrawals(self, cash_withdrawals):
        total_cash_withdrawals = 0
        for cash_withdrawal in cash_withdrawals:
            if(cash_withdrawal.get('amount')):
                total_cash_withdrawals += cash_withdrawal['amount']

        return total_cash_withdrawals

    def calculate_difference(self, session):
        print(session)

        difference = 0
        total_deposits = session['total_deposits']
        total_returns = session['total_returns']
        total_payments = session['total_payments']
        total_card_payments = session['total_card_payments']
        total_cash_withdrawals = session['total_cash_withdrawals']
        initial_money = session['initial_money']
        total_sales = session['total_sales']
        total_incomes = session['total_incomes']

        difference += total_deposits
        difference += total_returns
        difference += total_payments
        difference += total_card_payments
        difference += total_cash_withdrawals
        difference -= initial_money
        difference -= total_sales
        difference -= total_incomes

        return difference