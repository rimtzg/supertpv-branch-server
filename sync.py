import json
import requests

from config import app_config
from driver import database as db

from schemas.products import schema as schema_product

API_URL      = app_config['API']['URL']
API_ACCOUNT  = app_config['API']['ACCOUNT']
API_USERNAME = app_config['API']['USERNAME']
API_PASSWORD = app_config['API']['PASSWORD']
API_DELAY    = app_config['API']['DELAY']

class Sync:
    def __init__(self):
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

    def get_products(self):
        url = API_URL + '/products/'

        headers = {
            'Token' : self.token
        }

        response = requests.get(url, headers=headers)

        if(response):
            if(response.status_code == requests.codes.ok):
                data = json.loads(response.text)
                for product in data['data']:
                    db.products.insert(schema_product.validate(product))
