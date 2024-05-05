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

def sync_sales():
    logging.info('START SYNC SALES')

    DELAY = 120

    sales = Sales()

    while True:
        sales.upload()
            
        sleep(DELAY)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class Sales():
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

            sale = db.sales.find_one(query, sort=[("date", -1)])

            if(sale):
                logging.info('SYNC NEW SALE')

                sale['session_id'] = sale['session']

                url = '{}/sales/save?id={}'.format( server, sale['_id'] )

                data = DateTimeEncoder().encode(sale)

                response = None
                try:
                    response = requests.post(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : sale['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.sales.find_one_and_update(query, data)

                    return True

        return False