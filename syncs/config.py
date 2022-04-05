import logging
import requests
import json
from datetime import datetime
from time import sleep

# from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config, save_config_file

from schemas.cashiers import schema as cashier_schema

def sync_config():
    logging.info('START SYNC CONFIG')

    config = Config()

    while True:
        config.get()

        sleep(120)
    
class Config():
    def get(self):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            url = '{}/branchs/config'.format( server )

            headers = {
                'Token' : token
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):
                config = json.loads(response.text)
                
                logging.info('CONFIG: {}'.format( config ))

                if(config.get('can_delete')):
                    app_config['APP']['can_delete'] = str(config['can_delete'])
                else:
                    app_config['APP']['can_delete'] = 'False'

                if(config.get('phone')):
                    app_config['APP']['phone'] = config['phone']

                if(config.get('round_product')):
                    app_config['APP']['round_product'] = str(config['round_product'])
                else:
                    app_config['APP']['round_product'] = 'False'

                if(config.get('round_sale')):
                    app_config['APP']['round_sale'] = str(config['round_sale'])
                else:
                    app_config['APP']['round_sale'] = 'False'

                if(config.get('show_init_money')):
                    app_config['APP']['show_init_money'] = str(config['show_init_money'])
                else:
                    app_config['APP']['show_init_money'] = 'False'

                save_config_file()

                return True
                
        return False