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

from schemas.products import schema as schema_product
from schemas.products import modifications as modifications_product

from schemas.volume_discounts import schema as schema_volume_discount
from schemas.volume_discounts import modifications as modifications_volume_discount

class Sync(Server):
    def __init__(self):
        self.token = None
        # self.login()

        # self.get_products()

        # def get_updated_products():
        #     while True:
        #         self.login()

        #         date = app_config['API']['LAST_UPDATED']
        #         self.get_products(date)
                
        #         sleep(int(app_config['API']['DELAY']))

        # thread = threading.Thread(target=get_updated_products)
        # thread.start()

    # def get_updated_products(self):
    #     def get_updated_products():
    #         while True:
    #             #self.login()

    #             date = app_config['API']['LAST_UPDATED']

    #             if(len(date) == 0):
    #                 date = str(datetime.datetime.utcnow())

    #             self.get_products(date)
                
    #             sleep(int(app_config['API']['DELAY']))

    #     thread = threading.Thread(target=get_updated_products)
    #     thread.start()

    #     return None

    def login(self):
        url = app_config['API']['URL'] + '/token'

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
        business = app_config['API']['BUSINESS']
        branch = app_config['API']['BRANCH']

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
                        db.products.find_one_and_update({'_id' : _id }, {'$set' : schema_product.validate(product)}, upsert=True )

                    #GET PRODUCTS FROM BUSINESS
                    if not(date):
                        url = '{}/business/{}/products/'.format( server, business )
                    else:
                        url = '{}/business/{}/products/?date={}'.format( server, business, date )
                    logging.info(url)

                    try:
                        response = requests.get(url, headers=headers)
                    except:
                        response = None

                    if(response):
                        if(response.status_code == requests.codes.ok):

                            products = json.loads(response.text)
                            logging.info(len(products))

                            for product in products:
                                _id = ObjectId( product['document'] )
                                db.products.find_one_and_update({'_id' : _id }, {'$set' : modifications_product.validate(product)} )

                            if not(date):
                                url = '{}/business/{}/branch/{}/products/'.format( server, business, branch )
                            else:
                                url = '{}/business/{}/branch/{}/products/?date={}'.format( server, business, branch, date )
                            logging.info(url)

                            try:
                                response = requests.get(url, headers=headers)
                            except:
                                response = None

                            if(response):
                                if(response.status_code == requests.codes.ok):

                                    products = json.loads(response.text)
                                    logging.info(len(products))

                                    for product in products:
                                        _id = ObjectId( product['document'] )
                                        db.products.find_one_and_update({'_id' : _id }, {'$set' : modifications_product.validate(product)} )

    def get_volume_discount(self):
        server = app_config['API']['URL']
        business = app_config['API']['BUSINESS']
        branch = app_config['API']['BRANCH']

        try:
            db = Driver().database()
        except:
            db = None

        if not(self.token):
            self.login()

        if(db and self.token):
            headers = {
                'Token' : self.token
            }

            url = '{}/{}/'.format( server, 'volume_discounts' )
            logging.info(url)

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

                    url = '{}/business/{}/{}/'.format( server, business, 'volume_discounts' )
                    logging.info(url)

                    try:
                        response = requests.get(url, headers=headers)
                    except:
                        response = None

                    if(response):
                        if(response.status_code == requests.codes.ok):

                            discounts = json.loads(response.text)
                            logging.info(len(discounts))

                            for discount in discounts:
                                _id = ObjectId( discount['document'] )
                                db.volume_discounts.find_one_and_update({'_id' : _id }, {'$set' : modifications_volume_discount.validate(discount)}, upsert=True )

                            url = '{}/business/{}/branch/{}/{}/'.format( server, business, branch, 'volume_discounts' )
                            logging.info(url)

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

                                        _id = ObjectId( discount['document'] )
                                        db.volume_discounts.find_one_and_update({'_id' : _id }, {'$set' : modifications_volume_discount.validate(discount)}, upsert=True )
            








