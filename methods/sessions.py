import logging
from datetime import datetime

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from driver import mongo

class Methods():
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

        if(session):
            initial_money = session['init_money'] if session.get('init_money') else 0

        sales = list(mongo['sales'].find({'session' : _id}))
        
        total_sales = 0
        for sale in sales:
            if not(sale.get('canceled') and sale['canceled']):
                total_sales += sale['total']
        
        num_of_sales = sales.count()

        incomes = list(mongo['incomes'].find({'session' : _id}))
        
        total_incomes = 0
        for income in incomes:
            total_incomes += income['amount']

        payments = list(mongo['payments'].find({'session' : _id}))

        total_payments = 0
        for payment in payments:
            total_payments += payment['amount']

        deposits = list(mongo['deposits'].find({'session' : _id}))

        total_deposits = 0
        for deposit in deposits:
            total_deposits += deposit['total']

        returns = list(mongo['returns'].find({'session' : _id}))

        total_returns = 0
        for retur in returns:
            total_returns += retur['total']

        card_payments = list(mongo['card_payments'].find({'session' : _id}))

        total_card_payments = 0
        for card_payment in card_payments:
            if(card_payment.get('amount')):
                total_card_payments += card_payment['amount']

        cash_withdrawals = list(mongo['cash_withdrawals'].find({'session' : _id}))

        total_cash_withdrawals = 0
        for cash_withdrawal in cash_withdrawals:
            if(cash_withdrawal.get('amount')):
                total_cash_withdrawals += cash_withdrawal['amount']

        difference = total_deposits + total_returns + total_payments + total_card_payments + total_cash_withdrawals - initial_money - total_sales - total_incomes

        end_date = datetime.utcnow()

        data = {
            'initial_money' : initial_money,
            'total_sales' : total_sales,
            'num_of_sales' : num_of_sales,
            'total_incomes' : total_incomes,
            'total_payments' : total_payments,
            'total_deposits' : total_deposits,
            'total_returns' : total_returns,
            'total_card_payments' : total_card_payments,
            'total_cash_withdrawals' : total_cash_withdrawals,
            'difference' : difference,
            'end_date' : end_date,
            'closed' : True
        }

        session = mongo['sessions'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        session['payments'] = payments
        session['deposits'] = deposits
        session['incomes'] = incomes
        session['returns'] = returns
        session['card_payments'] = card_payments

        return session

    def list(self):
        data = request.args

        if(not data.get('cashier') ):
            abort(403)

        query = {
            'cashier' : ObjectId(data['cashier']),
            'closed' : True
        }

        sessions = list(mongo['sessions'].find( query ).limit(10).sort([("start_date", -1)]))

        for session in sessions:
            session['payments'] = list(mongo['payments'].find({'session' : session['_id']}))
            session['incomes'] = list(mongo['incomes'].find({'session' : session['_id']}))
            session['deposits'] = list(mongo['deposits'].find({'session' : session['_id']}))
            session['returns'] = list(mongo['returns'].find({'session' : session['_id']}))
            session['card_payments'] = list(mongo['card_payments'].find({'session' : session['_id']}))

        return sessions