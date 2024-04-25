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

def sync_incomes():
    logging.info('START SYNC INCOMES')

    DELAY = int(app_config['API']['DELAY'])

    incomes = Incomes()

    while True:
        incomes.upload_old()
        incomes.upload()
        # sales.upload()
            
        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class Incomes():
    def upload(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            query = {
                'uploaded' : { '$ne' : True }
            }

            headers = {
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            income = db.incomes.find_one(query, sort=[("date", -1)])

            if(income):
                logging.info('SYNC NEW SALE')

                income['session_id'] = income['session']

                url = '{}/incomes/save?id={}'.format( server, income['_id'] )

                data = DateTimeEncoder().encode(income)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : income['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.incomes.find_one_and_update(query, data)

                    return True

        return False

    def upload_old(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            query = {
                'uploaded' : { '$ne' : True },
                'type' : 'in'
            }

            headers = {
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            income = db.MoneyMovements.find_one(query, sort=[("date", -1)])

            # print(income)

            if(income):
                logging.info('SYNC OLD INCOME')

                session = db.Sessions.find_one({ '_id' : income['session'] })

                if(session):
                    # print(session)

                    cashier = db.cashiers.find_one({ '_id' : session['user_id'] })

                    # print(cashier)
                    if not(cashier):
                        cashier = {
                            '_id' : ObjectId(),
                            'name' : 'Cajero sin nombre'
                        }

                    data = {
                        'cashier_id'   : cashier['_id'],
                        'cashier_name' : cashier['name'],
                        'cashier'      : cashier['_id'],
                        'session_id'   : session['_id'],
                        'date'         : local_time.localize(income['date'], is_dst=None).astimezone(pytz.utc),
                        'amount'       : income['amount'],
                        'reason'       : income['razon'],
                    }

                    url = '{}/incomes/{}'.format( server, income['_id'] )

                    data = DateTimeEncoder().encode(data)

                    response = None
                    try:
                        response = requests.put(url, data=data, headers=headers)
                    except requests.exceptions.RequestException as err:
                        logging.exception(err)

                    if(response and response.status_code == requests.codes.ok):

                        query = {
                            '_id' : income['_id']
                        }

                        data = {
                            '$set' : {'uploaded' : True}
                        }

                        db.MoneyMovements.find_one_and_update(query, data)

                        return True

        return False