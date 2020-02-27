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
from schemas.products import changes_schema as changes_schema_product
from schemas.categories import schema as schema_category

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

    def get_updated_products(self):
        def get_updated_products():
            while True:
                self.login()

                date = app_config['API']['LAST_UPDATED']
                self.get_products(date)
                
                sleep(int(app_config['API']['DELAY']))

        thread = threading.Thread(target=get_updated_products)
        thread.start()

    def login(self):
        url = app_config['API']['URL'] + '/token'

        headers = {
            'Account'  : app_config['API']['ACCOUNT'],
            'Username' : app_config['API']['USERNAME'],
            'Password' : app_config['API']['PASSWORD'],
        }

        try:
            response = requests.get(url, headers=headers)
        except:
            response = None

        if(response):
            if(response.status_code == requests.codes.ok):
                data = json.loads(response.text)

                self.token = data['token']

    def get_products(self, date=None):
        db = Driver().database()

        if not(self.token):
            self.login()

        if not(date):
            url = app_config['API']['URL'] + '/products/?active=true'
        else:
            url = app_config['API']['URL'] + '/products/?active=true&date={}'.format(date)
        logging.info(url)

        headers = {
            'Token' : self.token
        }

        try:
            response = requests.get(url, headers=headers)
        except:
            response = None
        logging.info(url)

        if(response):
            if(response.status_code == requests.codes.ok):
                if not (date):
                    db.products.delete_many({})

                    products = json.loads(response.text)
                    logging.info(len(products))

                    for product in products:
                        db.products.insert(schema_product.validate(product))

                #GET PRODUCTS FROM BUSINESS
                business = app_config['API']['BUSINESS']
                if not(date):
                    url = app_config['API']['URL'] + '/business/{}/products/?active=true'.format( business )
                else:
                    url = app_config['API']['URL'] + '/business/{}/products/?active=true&date={}'.format( business, date )

                try:
                    response = requests.get(url, headers=headers)
                except:
                    response = None
                logging.info(url)

                if(response):
                    if(response.status_code == requests.codes.ok):

                        products = json.loads(response.text)
                        logging.info(len(products))

                        for product in products:
                            _id = ObjectId( product['product'] )
                            db.products.update({'_id' : _id }, {'$set' : changes_schema_product.validate(product)} )

                        business = app_config['API']['BUSINESS']
                        branch = app_config['API']['BRANCH']

                        if not(date):
                            url = app_config['API']['URL'] + '/business/{}/branch/{}/products/?active=true'.format( business, branch )
                        else:
                            url = app_config['API']['URL'] + '/business/{}/branch/{}/products/?active=true&date={}'.format( business, branch, date )

                        try:
                            response = requests.get(url, headers=headers)
                        except:
                            response = None
                        logging.info(url)

                        if(response):
                            if(response.status_code == requests.codes.ok):

                                products = json.loads(response.text)
                                logging.info(len(products))

                                for product in products:
                                    _id = ObjectId( product['product'] )
                                    db.products.update({'_id' : _id }, {'$set' : changes_schema_product.validate(product)} )

                                app_config['API']['LAST_UPDATED'] = str(datetime.datetime.utcnow())
                                save_config_file()







