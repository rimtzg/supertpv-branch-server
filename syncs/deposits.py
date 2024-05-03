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

def sync_deposits():
    logging.info('START SYNC DEPOSITS')

    DELAY = 120

    deposits = Deposits()

    while True:
        deposits.upload()
            
        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class Deposits():
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

            deposit = db.deposits.find_one(query, sort=[("date", -1)])

            if(deposit):
                logging.info('SYNC NEW SALE')

                deposit['session_id'] = deposit['session']

                url = '{}/deposits/save?id={}'.format( server, deposit['_id'] )

                data = DateTimeEncoder().encode(deposit)

                response = None
                try:
                    response = requests.post(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : deposit['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.deposits.find_one_and_update(query, data)

                    return True

        return False