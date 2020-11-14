from flask import session
from flask_script import Server
import json
from json import JSONEncoder
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
from schemas.cashiers import schema as schema_cashier
from schemas.sessions import schema as schema_session

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            if isinstance(obj, ObjectId):
                return str(obj)

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
            
    def get_cashiers(self, date=None):
        server = app_config['API']['URL']

        try:
            db = Driver().database()
        except:
            db = None

        if not(self.token):
            self.login()

        if(db and self.token):
            if not(date):
                url = '{}/cashiers/'.format( server )
            else:
                url = '{}/cashiers/?date={}'.format( server, date )
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

                    get_cashiers = json.loads(response.text)
                    logging.info(len(get_cashiers))

                    for cashier in get_cashiers:
                        #print(discount)

                        _id = ObjectId( cashier['_id'] )
                        db.cashiers.find_one_and_update({'_id' : _id }, {'$set' : schema_cashier.validate(cashier)}, upsert=True )

    def upload_session(self):
        logging.info('Upload sessions')

        server = app_config['API']['URL']

        logging.info(server)

        try:
            db = Driver().database()
        except:
            db = None

        logging.info(db)

        if not(self.token):
            self.login()

        logging.info(self.token)

        if(db and self.token):
            query = {
                'uploaded' : { '$ne' : True }
            }

            logging.info(query)

            headers = {
                'Token' : self.token,
                'Content-Type' : 'application/json'
            }

            logging.info(headers)

            sessions = db.Sessions.find(query).sort([("start", -1)]).limit(10)

            logging.info(sessions)

            for session in sessions:

                logging.info(session)

                _id = session['_id']
                initial_money = session['initial_money']

                start_date = session['start']
                if(session.get('end')):
                    end_date = session['end']
                else:
                    end_date = datetime.datetime.now()

                sales = db.Sales.find({'session': session['_id']})
                total_sales = 0
                for sale in sales:
                    total_sales += sale['total']

                money_movements = db.MoneyMovements.find({'session': session['_id']})
                total_incomes = 0
                total_expenses = 0
                for money in money_movements:
                    if(money['type'] == 'out'):
                        total_expenses += money['amount']
                    else:
                        total_incomes += money['amount']

                logging.info(total_incomes)
                logging.info(total_expenses)

                deposits = db.Deposits.find({'session._id': session['_id']})
                total_deposits = 0
                for deposit in deposits:
                    total_deposits += deposit['total']

                logging.info(total_deposits)

                card_payments = db.CardPayments.find({'session._id': session['_id']})
                total_card_payments = 0
                for payment in card_payments:
                    total_card_payments += payment['amount'] - payment['commission']

                logging.info(total_card_payments)
                
                returns = db.Returns.find({'session._id': session['_id']})
                total_returns = 0
                for ret in returns:
                    total_returns += ret['total']

                logging.info(total_returns)

                difference = total_deposits + total_returns + total_expenses +total_card_payments - initial_money - total_sales - total_incomes

                logging.info(difference)
                
                data = {
                    '_id'                 : _id,
                    'initial_money'       : initial_money,
                    'total_sales'         : total_sales,
                    'num_of_sales'        : len(session['sales']),
                    'total_incomes'       : total_incomes,
                    'total_expenses'      : total_expenses,
                    'total_deposits'      : total_deposits,
                    'total_returns'       : total_returns,
                    'total_card_payments' : total_card_payments,
                    'difference'          : difference,

                    'start_date'          : start_date,
                    'end_date'            : end_date,

                    'cashier'             : session['user_id']
                }

                logging.info(data)

                url = '{}/sessions/{}'.format( server, session['_id'] )
                logging.info(url)

                try:
                    response = requests.put(url, data=DateTimeEncoder().encode(data), headers=headers)
                except:
                    logging.exception('Error valuating data on modify')


