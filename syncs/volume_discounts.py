import logging
import requests
import json
from datetime import datetime
from time import sleep

from flask_script import Server
from bson.objectid import ObjectId

from driver import mongo
from config import app_config

from schemas.volume_discounts import schema as volume_discounts_schema

def sync_volume_discounts():
    logging.info('START SYNC VOLUME DISCOUNTS')

    DATE = datetime.utcnow().isoformat()
    DELAY = int(app_config['API']['DELAY'])
    DELAY_TIME = 0

    volume_discounts = VolumeDiscounts()

    volume_discounts.get()

    sleep(DELAY)

    while True:
        num = volume_discounts.get(DATE)

        DATE = datetime.utcnow().isoformat()

        if(num == 0):
            DELAY_TIME += DELAY
        else:
            DELAY_TIME = DELAY

        sleep(DELAY_TIME)
    
class VolumeDiscounts(Server):
    def get(self, date=None):
        server = app_config['API']['URL']
        token = app_config['API']['TOKEN']

        try:
            db = mongo
        except:
            db = None

        if(db and token):
            if(date):
                url = '{}/volume_discounts/?modified={}'.format( server, date )
            else:
                url = '{}/volume_discounts/'.format( server )

            headers = {
                'Token' : token
            }

            response = None
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.RequestException as err:
                logging.exception(err)

            if(response and response.status_code == requests.codes.ok):
                if not(date):
                    db.volume_discounts.delete_many({})

                volume_discounts = json.loads(response.text)
                logging.info('VOLUME DISCOUNTS: {}'.format( len(volume_discounts) ))

                for volume_discount in volume_discounts:
                    # logging.info(volume_discount)
                    _id = ObjectId( volume_discount['_id'] )
                    db.volume_discounts.find_one_and_update({'_id' : _id }, {'$set' : volume_discounts_schema.validate(volume_discount)}, upsert=True )

                return len(volume_discounts)
                
        return 0