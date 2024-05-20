import logging
import requests
import json
from datetime import datetime
from time import sleep

# from flask_script import Server
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
    DELAY = 120

    products = Products()

    products.get()
    products.deleted()
    
    sleep(DELAY)

    while True:
        num = products.get(DATE)
        
        DATE = datetime.utcnow().isoformat()

        if(num > 0):
            products.deleted()

        sleep(DELAY)
    
class Products():
    def get(self, date=None):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            if(date):
                url = '{}/products/branch?modified={}'.format( server, date )
            else:
                url = '{}/products/branch'.format( server )

            headers = {
                'Authorization' : f"Bearer {token}"
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):
                # if not(date):
                #     db.products.delete_many({})

                products = json.loads(response.text)
                logging.info('PRODUCTS: {}'.format( len(products) ))

                for product in products:
                    _id = ObjectId( product['_id'] )

                    query = {
                        '_id' : _id
                    }

                    data = {
                        '$set' : product_schema.validate(product)
                    }

                    db.products.find_one_and_update(query, data, upsert=True )

                return len(products)
                
        return 0

    def deleted(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            url = '{}/products/deleted'.format( server )

            headers = {
                'Authorization' : f"Bearer {token}"
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):
                products = json.loads(response.text)
                logging.info('DELETED PRODUCTS: {}'.format( len(products) ))

                for product in products:
                    _id = ObjectId( product['_id'] )

                    query = {
                        '_id' : _id
                    }

                    db.products.delete_one(query)