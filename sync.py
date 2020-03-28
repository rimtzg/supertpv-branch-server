from flask import session
from flask_script import Server
import json
import requests
import datetime
from bson.objectid import ObjectId
import logging
from time import sleep
import threading

from config import app_config, save_config_file
from driver import Driver

from schemas.products import schema as product_schema
from schemas.prices import schema as price_schema
from schemas.discounts import schema as discount_schema

from schemas.volume_discounts import schema as schema_volume_discount

class Sync(Server):
    def __init__(self):
        self.token = None

    def login(self):
        url = app_config['API']['URL'] + '/token/'

        headers = {
            'Account'  : app_config['API']['ACCOUNT'],
            'Username' : app_config['API']['USERNAME'],
            'Password' : app_config['API']['PASSWORD'],
            'Remember' : 'true',
        }

        try:
            response = requests.get(url, headers=headers)
        except:
            response = None

        if(response):
            if(response.status_code == requests.codes.ok):
                data = json.loads(response.text)

                self.token = data['token']

    def del_products(self):
        try:
            db = Driver().database()
        except:
            db = None

        if(db):
            db.products.delete_many({})

    def get_products(self, date=None):
        server = app_config['API']['URL']

        try:
            db = Driver().database()
        except:
            db = None

        if not(self.token):
            self.login()

        if(db and self.token):
            if not(date):
                url = '{}/products/'.format( server )
            else:
                url = '{}/products/?date={}'.format( server, date )
            logging.info(url)

            headers = {
                'Token' : self.token
            }

            try:
                response = requests.get(url, headers=headers)
            except:
                response = None

            if(response):
                if(response.status_code == requests.codes.ok):

                    products = json.loads(response.text)
                    logging.info(len(products))

                    for product in products:
                        _id = ObjectId( product['_id'] )
                        db.products.find_one_and_update({'_id' : _id }, {'$set' : product_schema.validate(product)}, upsert=True )

    def get_prices(self, date=None):
        server = app_config['API']['URL']

        try:
            db = Driver().database()
        except:
            db = None

        if not(self.token):
            self.login()

        if(db and self.token):
            if not(date):
                url = '{}/prices/'.format( server )
            else:
                url = '{}/prices/?date={}'.format( server, date )
            logging.info(url)

            headers = {
                'Token' : self.token
            }

            try:
                response = requests.get(url, headers=headers)
            except:
                response = None

            if(response):
                if(response.status_code == requests.codes.ok):

                    prices = json.loads(response.text)
                    logging.info(len(prices))

                    for price in prices:
                        _id = ObjectId( price['product'] )
                        db.products.find_one_and_update({'_id' : _id }, {'$set' : price_schema.validate(price)}, upsert=False )

    def get_discounts(self, date=None):
        server = app_config['API']['URL']

        try:
            db = Driver().database()
        except:
            db = None

        if not(self.token):
            self.login()

        if(db and self.token):
            if not(date):
                url = '{}/discounts/'.format( server )
            else:
                url = '{}/discounts/?date={}'.format( server, date )
            logging.info(url)

            headers = {
                'Token' : self.token
            }

            try:
                response = requests.get(url, headers=headers)
            except:
                response = None

            if(response):
                if(response.status_code == requests.codes.ok):

                    discounts = json.loads(response.text)
                    logging.info(len(discounts))

                    for discount in discounts:
                        _id = ObjectId( discount['product'] )
                        if(discount['volume_discount']):
                            volume_discount = ObjectId(discount['volume_discount'])
                        else:
                            volume_discount = None

                        data = {
                            'volume_discount' : volume_discount
                        }

                        db.products.find_one_and_update({'_id' : _id }, {'$set' : data}, upsert=False )

    def get_volume_discount(self, date=None):
        server = app_config['API']['URL']

        try:
            db = Driver().database()
        except:
            db = None

        if not(self.token):
            self.login()

        if(db and self.token):
            if not(date):
                url = '{}/volume_discounts/'.format( server )
            else:
                url = '{}/volume_discounts/?date={}'.format( server, date )
            logging.info(url)

            headers = {
                'Token' : self.token
            }

            try:
                response = requests.get(url, headers=headers)
            except:
                response = None

            if(response):
                if(response.status_code == requests.codes.ok):

                    discounts = json.loads(response.text)
                    logging.info(len(discounts))

                    for discount in discounts:
                        #print(discount)

                        _id = ObjectId( discount['_id'] )
                        db.volume_discounts.find_one_and_update({'_id' : _id }, {'$set' : schema_volume_discount.validate(discount)}, upsert=True )
            








