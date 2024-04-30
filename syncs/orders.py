import logging
import requests
import json
from datetime import datetime, timedelta
from time import sleep

# from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

from schemas.orders import Orders as OrderSchema

def sync_orders():
    logging.info('START SYNC ORDERS')

    date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

    orders = Orders()
    orders.get(date)

    while True:
        date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        orders.get(date)

        sleep(120)
    
class Orders():
    def get(self, date=None):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            url = f'{server}/orders/list?start={date}'

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
                    db.orders.delete_many({})

                orders = json.loads(response.text)
                logging.info('ORDERS: {}'.format( len(orders) ))

                for order in orders:
                    # logging.info(order)

                    _id = ObjectId( order['_id'] )
                    db.orders.find_one_and_update({'_id' : _id }, {'$set' : OrderSchema.validate(order)}, upsert=True )