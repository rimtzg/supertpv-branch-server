import logging
import requests
import json
from datetime import datetime, date
from time import sleep
from json import JSONEncoder

from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

def sync_recharges():
    logging.info('START SYNC RECHARGES')

    # DATE = datetime.utcnow().isoformat()
    DELAY = int(app_config['API']['DELAY'])
    DELAY_TIME = 0

    recharges = Recharges()

    while True:
        ok = recharges.upload()

        if not(ok):
            DELAY_TIME += DELAY
        else:
            DELAY_TIME = DELAY

        print(DELAY_TIME)
        sleep(DELAY_TIME)

class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (date, datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

class Recharges(Server):
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

            document = db.Recharges.find_one(query, sort=[("date", -1)])

            if(document):

                recharge = {
                    '_id'           : document['_id'],
                    'company'       : document['company'],
                    'amount'        : document['amount'],
                    'number'        : document['number'],
                    'date'          : document['date'],
                    'cashier_id'    : document['user_id'],
                    'cashier_name'  : document['name'],
                    'session'       : document['session'],
                    'sale'          : document['sale_id'],
                    'info'          : document['info'],
                    'status'        : document['status']
                }

                url = '{}/recharges/{}'.format( server, recharge['_id'] )

                data = DateTimeEncoder().encode(recharge)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : recharge['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.Recharges.find_one_and_update(query, data)

                    return True

        return False