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

    # DELAY = int(app_config['API']['DELAY'])

    sessions = Sessions()

    while True:
        sessions.upload_old()
        sessions.upload_actual_old()
        sessions.upload()
        sessions.upload_actual()
            
        sleep(120)

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
                    response = requests.put(url, data=data, headers=headers)
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

                difference = total_deposits + total_returns + total_payments + total_card_payments - initial_money - total_sales - total_incomes

                # logging.info(difference)
                
                data = {
                    '_id'                 : _id,
                    'initial_money'       : initial_money,
                    'total_sales'         : total_sales,
                    'num_of_sales'        : sales.count(),
                    'total_incomes'       : total_incomes,
                    'total_payments'      : total_payments,
                    'total_deposits'      : total_deposits,
                    'total_returns'       : total_returns,
                    'total_card_payments' : total_card_payments,
                    'difference'          : difference,

                    'start_date'          : start_date,
                    'end_date'            : end_date,

                    'cashier_id'          : cashier['_id'],
                    'cashier_name'        : cashier['name']
                }

                data = DateTimeEncoder().encode(data)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):
                    return True

        return False

    def upload_actual_old(self):
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
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            session = db.Sessions.find_one(query, sort=[("start", -1)])

            if(session):
                logging.info('SYNC ACTUAL OLD SESSION')

                url = '{}/sessions/{}'.format( server, session['_id'] )

                _id = session['_id']

                initial_money = 0
                if(session.get('initial_money')):
                    initial_money = session['initial_money']

                #local_datetime = local_time.localize(naive_datetime, is_dst=None)
                start_date = local_time.localize(session['start'], is_dst=None).astimezone(pytz.utc)
                if(session.get('end')):
                    end_date = local_time.localize(session['end'], is_dst=None).astimezone(pytz.utc)
                else:
                    end_date = None

                sales = db.Sales.find({'session': session['_id'], 'canceled' : { '$ne' : True }})
                total_sales = 0
                for sale in sales:
                    if(sale.get('total')):
                        total_sales += sale['total']
                    else:
                        total_sales += 0

                money_movements = db.MoneyMovements.find({'session': session['_id']})
                total_incomes = 0
                total_expenses = 0
                for money in money_movements:
                    if(money.get('type') and money['type'] == 'out'):
                        total_expenses += money['amount']
                    else:
                        total_incomes += money['amount']

                # logging.info(total_incomes)
                # logging.info(total_expenses)

                deposits = db.Deposits.find({'session._id': session['_id']})
                total_deposits = 0
                for deposit in deposits:
                    total_deposits += deposit['total']

                # logging.info(total_deposits)

                card_payments = db.CardPayments.find({'session._id': session['_id']})
                total_card_payments = 0
                for payment in card_payments:
                    total_card_payments += payment['amount'] - payment['commission']

                # logging.info(total_card_payments)
                
                returns = db.Returns.find({'session._id': session['_id']})
                total_returns = 0
                for ret in returns:
                    total_returns += ret['total']

                # logging.info(total_returns)

                difference = total_deposits + total_returns + total_expenses + total_card_payments - initial_money - total_sales - total_incomes

                # logging.info(difference)
                
                data = {
                    '_id'                 : _id,
                    'initial_money'       : initial_money,
                    'total_sales'         : total_sales,
                    'num_of_sales'        : len(session['sales']),
                    'total_incomes'       : total_incomes,
                    'total_payments'      : total_expenses,
                    'total_deposits'      : total_deposits,
                    'total_returns'       : total_returns,
                    'total_card_payments' : total_card_payments,
                    'difference'          : difference,

                    'start_date'          : start_date,
                    'end_date'            : end_date,

                    'cashier_id'          : session['user_id'],
                    'cashier_name'        : session['name']
                }

                data = DateTimeEncoder().encode(data)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):
                    return True

        return False