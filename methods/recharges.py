import logging
from datetime import datetime

import urllib.request
import urllib.parse
import hashlib
import xml.etree.ElementTree as ET

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from driver import mongo
from config import app_config

def computeMD5hash(my_string):
    m = hashlib.md5()
    m.update(my_string.encode('utf-8'))
    return m.hexdigest()

class Recharges():
    def save(self):
        _id = ObjectId()
        args = request.args
        service = request.json
        data = service['data']

        if(not args.get('session') ):
            abort(403)

        if(not args.get('cashier') ):
            abort(401)

        if(not args.get('sale') ):
            abort(401)

        query = {
            '_id' : _id,
        }

        cashier = mongo['cashiers'].find_one({'_id' : ObjectId(args['cashier'])})

        if not(cashier):
            abort(401)

        data['session'] = ObjectId(args['session'])
        data['cashier_id'] = cashier['_id']
        data['cashier_name'] = cashier['name']
        data['sale'] = ObjectId(args['sale'])
        data['total'] = service['total']

        recharge = self.send_recharge(data['company'], data['number'], data['amount'])

        data['date'] = recharge['date']
        data['info'] = recharge['info']
        data['status'] = recharge['status']

        document = mongo['recharges'].find_one_and_update(query, {"$set": data}, upsert=True, return_document=ReturnDocument.AFTER)

        if(document['status'] != True):
            self.return_recharge(document)

        return document

    def send_recharge(self, company, number, amount):
        USERNAME = app_config['APP']['username_recharges']
        PASSWORD = app_config['APP']['password_recharges']
        URL = app_config['APP']['url_recharges']
        response = None
        request = None
        data = None
        new_xml = None

        logging.debug('Usuario: ' + USERNAME)
        logging.debug('Password: ' + PASSWORD)

        try:
            request = urllib.request.Request(URL)
        except urllib.error.URLError as e:
            self.log.error(e)

        logging.debug('Request: ' + str(request))

        data = {}
        data['date'] = datetime.utcnow()
        data['info'] = None
        data['status'] = False

        if(request):
            xml = '''<?xml version='1.0' encoding='utf-8'?>
            <operation>Compra</operation>
            <user>USERNAME</user>
            <password>PASSWORD</password>
            <Carrier>COMPANY</Carrier>
            <Monto>AMOUNT</Monto>
            <Telefono>NUMBER</Telefono>
            '''.replace('USERNAME', USERNAME).replace('PASSWORD', computeMD5hash(PASSWORD)).replace('COMPANY', company).replace('AMOUNT', str(amount)).replace('NUMBER', number)

            logging.debug('XML: ' + xml)

            request.add_header('Content-Type', 'application/xml')
            response = urllib.request.urlopen(request, data=xml.encode('utf-8'))

            if(response):
                logging.debug('Status: ' + str(response.status))
                logging.debug('Message: ' + response.msg)

                result = response.read()

                if(result):
                    logging.debug('Result: ' + str(result))

                    root = ET.fromstring(result)

                    for child in root.iter('resultado'):
                        #new_xml = child.text
                        new_xml = '<?xml version="1.0" encoding="utf-8"?><data>' + child.text + '</data>'

                    if(new_xml):
                        logging.debug(new_xml)
                        result = ET.XML(new_xml)
                        operation = result.find('operation').text

                        if(operation != 'Error'):
                            data['info'] = "Recarga realizada, Folio: {}".format(result.find('auth1').text)
                            data['status'] = True
                        else:
                            data['info'] = result.find('result').text
                    else:
                        data['info'] = 'Error al leer los datos del servidor'
                else:
                    data['info'] = 'No se recibieron datos del servidor'
            else:
                data['info'] = response.msg
        else:
            data['info'] = 'Error al realizar la conexion con el servidor'

        return data

    def return_recharge(self, data):
        _id = ObjectId()

        data['sale'] = data['sale']
        data['_id'] = _id

        data['date'] = datetime.utcnow()

        data['session'] = data['session']
        data['cashier'] = data['cashier_id']
        data['cashier_id'] = data['cashier_id']
        data['cashier_name'] = data['cashier_name']
        data['reason'] = data['info']
        data['total'] = data['total']

        number = mongo['returns'].find({"number" : { '$exists': True }}).count()+1

        data['number'] = number

        query = {
            '_id' : _id
        }

        document = mongo['returns'].find_one_and_update(query, {'$set': data}, upsert=True, return_document=ReturnDocument.AFTER)

        # query_sale = {
        #     '_id' : data['sale']
        # }
        # mongo['sales'].find_one_and_update(query_sale, {'$set': { 'returned' : True }})

        return document