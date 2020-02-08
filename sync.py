from flask import session
import json
import requests
import datetime
from bson.objectid import ObjectId
import logging

from config import app_config, save_config_file
from driver import database as db

from schemas.products import schema as schema_product
from schemas.products import changes_schema as changes_schema_product
from schemas.categories import schema as schema_category

API_URL      = app_config['API']['URL']
API_ACCOUNT  = app_config['API']['ACCOUNT']
API_USERNAME = app_config['API']['USERNAME']
API_PASSWORD = app_config['API']['PASSWORD']
API_DELAY    = app_config['API']['DELAY']

class Sync:
    def __init__(self):
        self.token = None

    def login(self):
        url = API_URL + '/token'

        headers = {
            'Account'  : API_ACCOUNT,
            'Username' : API_USERNAME,
            'Password' : API_PASSWORD,
        }

        response = requests.get(url, headers=headers)

        if(response):
            if(response.status_code == requests.codes.ok):
                data = json.loads(response.text)

                self.token = data['token']

    def get_all_products(self):
        if not(self.token):
            self.login()

        url = API_URL + '/products/?active=true'

        headers = {
            'Token' : self.token
        }

        response = requests.get(url, headers=headers)
        logging.info(url)

        if(response):
            if(response.status_code == requests.codes.ok):
                db.products.delete_many({})

                products = json.loads(response.text)
                logging.info(len(products))

                for product in products:
                    db.products.insert(schema_product.validate(product))

                #GET PRODUCTS FROM BUSINESS
                business = app_config['API']['BUSINESS']
                url = API_URL + '/business/{}/products/?active=true'.format( business )

                response = requests.get(url, headers=headers)
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

    def get_updated_products(self):
        if not(self.token):
            self.login()
            
        date = app_config['API']['LAST_UPDATED']

        url = API_URL + '/products/?active=true&date={}'.format(date)
        logging.info(url)

        headers = {
            'Token' : self.token
        }

        response = requests.get(url, headers=headers)

        if(response):
            if(response.status_code == requests.codes.ok):

                products = json.loads(response.text)

                print(len(products))
                for product in products:
                    product = schema_product.validate(product)
                    db.products.find_one_and_update({'_id' : product['_id']}, {'$set' : product})

                app_config['API']['LAST_UPDATED'] = str(datetime.datetime.utcnow())
                save_config_file()









