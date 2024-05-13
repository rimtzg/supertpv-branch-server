import logging
import requests
import json
from datetime import datetime, date
from time import sleep
from json import JSONEncoder

import pytz
local_time = pytz.timezone("America/Mexico_City")

# from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

def sync_sessions():
    logging.info('START SYNC SESSIONS')

    DELAY = 120

    sessions = Sessions()

    while True:
        sessions.upload()
        sessions.upload_actual()

        DELAY += 5
            
        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class Sessions():
    def upload(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            query = {
                'uploaded' : { '$ne' : True },
                'closed' : True,
            }

            headers = {
                'Authorization' : f"Bearer {token}",
                'Content-Type' : 'application/json'
            }

            session = db.sessions.find_one(query, sort=[("start_date", -1)])

            if(session):
                logging.info('SYNC NEW SESSION')

                cashier = db.cashiers.find_one({'_id' : session['cashier_id']})

                if(cashier):
                    session['cashier_id'] = cashier['_id']
                    session['cashier_name'] = cashier['name']
                else:
                    session['cashier_id'] = session['cashier_id']
                    session['cashier_name'] = 'Sin nombre'

                url = '{}/sessions/save?id={}'.format( server, session['_id'] )

                data = DateTimeEncoder().encode(session)

                response = None
                try:
                    response = requests.post(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : session['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.sessions.find_one_and_update(query, data)

                    return True

        return False

    def upload_actual(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            query = {
                'closed' : { '$ne' : True },
            }

            headers = {
                'Authorization' : f"Bearer {token}",
                'Content-Type' : 'application/json'
            }

            session = db.sessions.find_one(query, sort=[("start_date", -1)])

            if(session):
                logging.info('SYNC ACTUAL SESSION')

                url = '{}/sessions/save?id={}'.format( server, session['_id'] )

                _id = session['_id']

                cashier = db.cashiers.find_one({'_id' : session['cashier_id']})

                if not(cashier):
                    cashier = {}
                    cashier['_id'] = None
                    cashier['name'] = 'Cajero'

                initial_money = 0
                if(session.get('initial_money')):
                    initial_money = session['initial_money']

                #local_datetime = local_time.localize(naive_datetime, is_dst=None)
                start_date = session['start_date']
                if(session.get('end_date')):
                    end_date = session['end_date']
                else:
                    end_date = None

                sales = db.sales.find({'session': session['_id'], 'canceled' : { '$ne' : True }})
                total_sales = 0
                for sale in sales:
                    if(sale.get('total')):
                        total_sales += sale['total']
                    else:
                        total_sales += 0

                incomes = db.incomes.find({'session': session['_id']})
                total_incomes = 0
                for income in incomes:
                    total_incomes += income['amount']

                payments = db.payments.find({'session': session['_id']})
                total_payments = 0
                for payment in payments:
                    total_payments += payment['amount']

                deposits = db.deposits.find({'session': session['_id']})
                total_deposits = 0
                for deposit in deposits:
                    total_deposits += deposit['total']

                returns = db.returns.find({'session': session['_id']})
                total_returns = 0
                for ret in returns:
                    total_returns += ret['total']

                card_payments = db.card_payments.find({'session': session['_id']})
                total_card_payments = 0
                for payment in card_payments:
                    total_card_payments += payment['amount']

                cash_withdrawals = db.cash_withdrawals.find({'session': session['_id']})
                total_cash_withdrawals = 0
                for cash_withdrawal in cash_withdrawals:
                    total_cash_withdrawals += cash_withdrawal['amount']

                difference = total_deposits + total_returns + total_payments + total_card_payments - initial_money - total_sales - total_incomes + total_cash_withdrawals

                # logging.info(difference)
                
                data = {
                    '_id'                 : _id,
                    'initial_money'       : initial_money,

                    'total_sales'               : total_sales,
                    'total_incomes'             : total_incomes,
                    'total_payments'            : total_payments,
                    'total_deposits'            : total_deposits,
                    'total_returns'             : total_returns,
                    'total_card_payments'       : total_card_payments,
                    'total_cash_withdrawals'    : total_cash_withdrawals,

                    'difference'          : difference,
                    
                    'num_of_sales'              : sales.count(),
                    'num_of_returns'            : returns.count(),
                    'num_of_payments'           : payments.count(),
                    'num_of_incomes'            : incomes.count(),
                    'num_of_deposits'           : deposits.count(),
                    'num_of_card_payments'      : card_payments.count(),
                    'num_of_cash_withdrawals'   : cash_withdrawals.count(),

                    'start_date'          : start_date,
                    'end_date'            : end_date,

                    'cashier_id'          : cashier['_id'],
                    'cashier_name'        : cashier['name']
                }

                data = DateTimeEncoder().encode(data)

                response = None
                try:
                    response = requests.post(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):
                    return True

        return False