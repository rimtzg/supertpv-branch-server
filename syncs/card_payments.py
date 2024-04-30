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
from config import app_config, save_config_file

def sync_card_payments():
    logging.info('START SYNC CARD PAYMENTS')

    DELAY = 120

    card_payments = CardPayments()

    while True:
        card_payments.upload()
            
        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class CardPayments():
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
                'Authorization' : f"Bearer {token}",
                'Content-Type' : 'application/json'
            }

            card_payment = db.card_payments.find_one(query, sort=[("date", -1)])

            if(card_payment):
                logging.info('SYNC NEW SALE')

                if(card_payment.get('session')):
                    card_payment['session_id'] = card_payment['session']

                    url = '{}/card_payments/save?id={}'.format( server, card_payment['_id'] )

                    data = DateTimeEncoder().encode(card_payment)

                    response = None
                    try:
                        response = requests.post(url, data=data, headers=headers)
                    except requests.exceptions.RequestException as err:
                        logging.exception(err)

                    if(response and response.status_code == requests.codes.ok):

                        query = {
                            '_id' : card_payment['_id']
                        }

                        data = {
                            '$set' : {'uploaded' : True}
                        }

                        db.card_payments.find_one_and_update(query, data)

                        return True

        return False