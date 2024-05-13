import logging
import requests
import json
from datetime import datetime
from time import sleep

# from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

from schemas.cashiers import schema as cashier_schema

def sync_cashiers():
    logging.info('START SYNC CASHIERS')

    DATE = datetime.utcnow().isoformat()
    DELAY = 120

    cashiers = Cashiers()

    cashiers.get()

    sleep(DELAY)

    while True:
        num = cashiers.get(DATE)

        DATE = datetime.utcnow().isoformat()

        DELAY += 5
        if(num > 0):
            DELAY = 120

        sleep(DELAY)
    
class Cashiers():
    def get(self, date=None):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            if(date):
                url = '{}/cashiers/branch?modified={}'.format( server, date )
            else:
                url = '{}/cashiers/branch'.format( server )

            headers = {
                'Authorization' : f"Bearer {token}"
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):
                if not(date):
                    db.cashiers.delete_many({})

                cashiers = json.loads(response.text)
                logging.info('CASHIERS: {}'.format( len(cashiers) ))

                for cashier in cashiers:
                    # logging.info(cashier)
                    _id = ObjectId( cashier['_id'] )
                    db.cashiers.find_one_and_update({'_id' : _id }, {'$set' : cashier_schema.validate(cashier)}, upsert=True )

                return len(cashiers)
                
        return 0