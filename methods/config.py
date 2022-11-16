import logging
from datetime import datetime

from flask import abort, request
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from config import app_config

class Methods():
    def get(self):

        data = {
            'business_name' : app_config['APP']['business_name'] if app_config['APP'].get('business_name') else 'SuperTPV',
            'can_delete' : app_config.getboolean('APP', 'can_delete'),
            'phone' : app_config['APP']['phone'] if app_config['APP'].get('phone') else '',
            'round_product' : app_config.getboolean('APP', 'round_product'),
            'round_sale' : app_config.getboolean('APP', 'round_sale'),
            'show_sessions' : app_config.getboolean('APP', 'show_sessions'),
            'show_init_money' : app_config.getboolean('APP', 'show_init_money'),
            'has_services' : app_config.getboolean('APP', 'has_services'),
            'ticket_min' : app_config.getint('APP', 'ticket_min') if app_config['APP'].get('ticket_min') else 0,
        }
        
        return data