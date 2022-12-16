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

                if(config.get('full_name')):
                    app_config['APP']['business_name'] = config['full_name']

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

                if(config.get('show_sessions')):
                    app_config['APP']['show_sessions'] = str(config['show_sessions'])
                else:
                    app_config['APP']['show_sessions'] = 'False'

                if(config.get('show_init_money')):
                    app_config['APP']['show_init_money'] = str(config['show_init_money'])
                else:
                    app_config['APP']['show_init_money'] = 'False'

                if(config.get('has_services')):
                    app_config['APP']['has_services'] = str(config['has_services'])
                else:
                    app_config['APP']['has_services'] = 'False'

                if(config.get('has_recharges')):
                    app_config['APP']['has_recharges'] = str(config['has_recharges'])
                else:
                    app_config['APP']['has_recharges'] = 'False'

                if(config.get('recharges_commission')):
                    app_config['APP']['recharges_commission'] = str(config['recharges_commission'])
                else:
                    app_config['APP']['recharges_commission'] = '0'

                if(config.get('url_recharges')):
                    app_config['APP']['url_recharges'] = config['url_recharges']

                if(config.get('username_recharges')):
                    app_config['APP']['username_recharges'] = config['username_recharges']

                if(config.get('password_recharges')):
                    app_config['APP']['password_recharges'] = config['password_recharges']

                if(config.get('has_pins')):
                    app_config['APP']['has_pins'] = str(config['has_pins'])
                else:
                    app_config['APP']['has_pins'] = 'False'

                if(config.get('has_cash_withdrawals')):
                    app_config['APP']['has_cash_withdrawals'] = str(config['has_cash_withdrawals'])
                else:
                    app_config['APP']['has_cash_withdrawals'] = 'False'

                if(config.get('ticket_min')):
                    app_config['APP']['ticket_min'] = str(config['ticket_min'])
                else:
                    app_config['APP']['ticket_min'] = '0'

                if(config.get('card_commission')):
                    app_config['APP']['card_commission'] = str(config['card_commission'])
                else:
                    app_config['APP']['card_commission'] = '0'

                if(config.get('withdrawal_commission')):
                    app_config['APP']['withdrawal_commission'] = str(config['withdrawal_commission'])
                else:
                    app_config['APP']['withdrawal_commission'] = '0'

                if(config.get('apply_withdrawal_commission')):
                    app_config['APP']['apply_withdrawal_commission'] = str(config['apply_withdrawal_commission'])
                else:
                    app_config['APP']['apply_withdrawal_commission'] = '0'

                if(config.get('has_card_payment')):
                    app_config['APP']['has_card_payment'] = str(config['has_card_payment'])
                else:
                    app_config['APP']['has_card_payment'] = 'False'

                if(config.get('has_orders')):
                    app_config['APP']['has_orders'] = str(config['has_orders'])
                else:
                    app_config['APP']['has_orders'] = 'False'

                if(config.get('min_withdrawal_commission')):
                    app_config['APP']['min_withdrawal_commission'] = str(config['min_withdrawal_commission'])
                else:
                    app_config['APP']['min_withdrawal_commission'] = '0'

                if(config.get('max_withdrawal_commission')):
                    app_config['APP']['max_withdrawal_commission'] = str(config['max_withdrawal_commission'])
                else:
                    app_config['APP']['max_withdrawal_commission'] = '0'

                save_config_file()

                return True
                
        return False