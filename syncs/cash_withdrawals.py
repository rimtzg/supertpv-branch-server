import logging
import requests
import json
from datetime import datetime, date
from time import sleep
from json import JSONEncoder

# from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

def sync_cash_withdrawals():
    logging.info('START SYNC CASH WITHDRAWLS')

    DELAY = int(app_config['API']['DELAY'])

    cash_withdrawals = CashWithdrawals()

    while True:
        cash_withdrawals.upload()

        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)

class CashWithdrawals():
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
            }

            headers = {
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            document = db.cash_withdrawals.find_one(query, sort=[("date", -1)])

            if(document):

                # cash_withdrawl = {
                #     '_id'           : document['_id'],
                #     'company'       : document['company'],
                #     'amount'        : document['amount'],
                #     'number'        : document['number'],
                #     'date'          : document['date'],
                #     'cashier_id'    : document['cashier_id'],
                #     'cashier_name'  : document['cashier_name'],
                #     'session'       : document['session'],
                #     'sale'          : document['sale'],
                #     'info'          : document['info'],
                #     'status'        : document['status']
                # }

                url = '{}/cash_withdrawals/{}'.format( server, document['_id'] )

                data = DateTimeEncoder().encode(document)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : document['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.cash_withdrawals.find_one_and_update(query, data)

                    return True

        return False