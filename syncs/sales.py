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

    DELAY = int(app_config['API']['DELAY'])

    sales = Sales()

    while True:
        sales.upload_old()
        sales.upload()
            
        sleep(5)

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
                    response = requests.put(url, data=data, headers=headers)
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
                'closed' : True,
            }

            headers = {
                'Token' : token,
                'Content-Type' : 'application/json'
            }

            sale = db.Sales.find_one(query, sort=[("date", -1)])

            if(sale):
                logging.info('SYNC OLD SALE')

                products = []

                for prod in sale['products']:
                    
                    _id = None
                    if(sale['products'][prod].get('_id')):
                        _id = sale['products'][prod]['_id']

                    code = ''
                    if(sale['products'][prod].get('code')):
                        code = sale['products'][prod]['code']

                    name = ''
                    if(sale['products'][prod].get('name')):
                        name = sale['products'][prod]['name']

                    cost = 0
                    if(sale['products'][prod].get('cost')):
                        cost = sale['products'][prod]['cost']

                    price = 0
                    if(sale['products'][prod].get('price')):
                        price = sale['products'][prod]['price']

                    amount = 0
                    if(sale['products'][prod].get('amount')):
                        amount = sale['products'][prod]['amount']

                    subtotal = 0
                    if(sale['products'][prod].get('subtotal')):
                        subtotal = sale['products'][prod]['subtotal']

                    product = {
                        '_id' : _id,
                        'code' : code,
                        'name' : name,
                        'cost' : cost,
                        'price' : price,
                        'amount' : amount,
                        'subtotal' : subtotal,
                    }

                    products.append(product)

                if(sale.get('ticket')):
                    ticket = sale['ticket']
                else:
                    ticket = None

                if(sale.get('canceled')):
                    canceled = sale['canceled']
                else:
                    canceled = None

                date = None
                if(sale.get('date')):
                    date = sale['date']

                    try:
                        date = local_time.localize(sale['date'], is_dst=None).astimezone(pytz.utc)
                    except pytz.exceptions.NonExistentTimeError as err:
                        logging.exception(err)

                data = {
                    '_id' : sale['_id'],
                    'date' : date,
                    'cashier_id' : sale['cashier_id'],
                    'cashier_name' : sale['cashier_name'],
                    'canceled' : canceled,
                    'session_id' : sale['session'],
                    'total' : sale['total'],
                    'ticket' : ticket,
                    'products' : products,
                    'num_of_products' : len(products)
                }

                url = '{}/sales/{}'.format( server, sale['_id'] )

                data = DateTimeEncoder().encode(data)

                response = None
                try:
                    response = requests.put(url, data=data, headers=headers)
                except requests.exceptions.RequestException as err:
                    logging.exception(err)

                if(response and response.status_code == requests.codes.ok):

                    query = {
                        '_id' : sale['_id']
                    }

                    data = {
                        '$set' : {'uploaded' : True}
                    }

                    db.Sales.find_one_and_update(query, data)

                    return True

        return False