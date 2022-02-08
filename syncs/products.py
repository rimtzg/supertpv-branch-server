import logging
import requests
import json
from datetime import datetime
from time import sleep

from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

from schemas.products import schema as product_schema
from schemas.prices import schema as price_schema
from schemas.discounts import schema as discount_schema
from schemas.stock import schema as stock_schema

def sync_products():
    logging.info('START SYNC PRODUCTS')

    DATE = datetime.utcnow().isoformat()
    DELAY = int(app_config['API']['DELAY'])
    DELAY_TIME = 0

    products = Products()

    products.get()
    products.prices()
    products.discounts()
    products.stock()
    
    sleep(DELAY)

    while True:
        num = products.get(DATE)

        if(num > 0):
            products.prices()
            products.discounts()
            products.stock()

        DATE = datetime.utcnow().isoformat()

        if(num == 0):
            DELAY_TIME += DELAY
        else:
            DELAY_TIME = DELAY

        sleep(DELAY_TIME)
    
class Products(Server):
    def get(self, date=None):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            if(date):
                url = '{}/products/?modified={}'.format( server, date )
            else:
                url = '{}/products/'.format( server )

            headers = {
                'Token' : token
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):
                if not(date):
                    db.products.delete_many({})

                products = json.loads(response.text)
                logging.info('PRODUCTS: {}'.format( len(products) ))

                for product in products:
                    
                    query = {
                        '_id' : ObjectId( product['_id'] )
                    }

                    data = {
                        '$set' : product_schema.validate(product)
                    }

                    db.products.find_one_and_update(query, data, upsert=True )

                return len(products)
                
        return 0

    def prices(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            url = '{}/prices/branch'.format( server )

            headers = {
                'Token' : token
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):

                prices = json.loads(response.text)
                logging.info('PRICES: {}'.format( len(prices) ))

                for price in prices:
                    if(price.get('product_id')):

                        query = {
                            '_id' : ObjectId( price['product_id'] )
                        }

                        data = {
                            '$set' : price_schema.validate(price)
                        }

                        db.products.find_one_and_update(query, data)

    def discounts(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            url = '{}/discounts/branch'.format( server )

            headers = {
                'Token' : token
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):

                discounts = json.loads(response.text)
                logging.info('DISCOUNTS: {}'.format( len(discounts) ))

                for discount in discounts:
                    if(discount.get('product_id')):

                        query = {
                            '_id' : ObjectId( discount['product_id'] )
                        }

                        data = {
                            '$set' : {
                                'volume_discount' : ObjectId(discount['volume_discount'])
                            }
                        }

                        db.products.find_one_and_update(query, data)

    def stock(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            url = '{}/stock/branch'.format( server )

            headers = {
                'Token' : token
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):

                stocks = json.loads(response.text)
                logging.info('STOCK: {}'.format( len(stocks) ))

                for stock in stocks:
                    if(stock.get('product')):

                        query = {
                            '_id' : ObjectId( stock['product'] )
                        }

                        data = {
                            '$set' : stock_schema.validate(stock)
                        }

                        db.products.find_one_and_update(query, data)