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
            
            'has_pins' : app_config.getboolean('APP', 'has_pins'),
            'has_cash_withdrawals' : app_config.getboolean('APP', 'has_cash_withdrawals'),
            'ticket_min' : app_config.getint('APP', 'ticket_min') if app_config['APP'].get('ticket_min') else 0,
            'card_commission' : app_config.getint('APP', 'card_commission') if app_config['APP'].get('card_commission') else 0,
            'withdrawal_commission' : app_config.getint('APP', 'withdrawal_commission') if app_config['APP'].get('withdrawal_commission') else 0,
            'apply_withdrawal_commission' : app_config.getint('APP', 'apply_withdrawal_commission') if app_config['APP'].get('apply_withdrawal_commission') else 0,
            'has_card_payment' : app_config.getboolean('APP', 'has_card_payment'),
            'has_orders' : app_config.getboolean('APP', 'has_orders'),
            'has_labels' : app_config.getboolean('APP', 'has_labels'),

            'min_withdrawal_commission' : app_config.getint('APP', 'min_withdrawal_commission') if app_config['APP'].get('min_withdrawal_commission') else 0,
            'max_withdrawal_commission' : app_config.getint('APP', 'max_withdrawal_commission') if app_config['APP'].get('max_withdrawal_commission') else 0,

            #APP
            'show_shortcuts' : app_config.getboolean('APP', 'show_shortcuts'),

            #RECHARGES
            'has_recharges' : app_config.getboolean('APP', 'has_recharges'),
            'recharges_commission' : app_config.getint('APP', 'recharges_commission') if app_config['APP'].get('recharges_commission') else 0,
            'username_recharges' : app_config['APP']['username_recharges'] if app_config['APP'].get('username_recharges') else '',
            'password_recharges' : app_config['APP']['password_recharges'] if app_config['APP'].get('password_recharges') else '',

            #TICEKTS
            'num_tickets' : app_config.getint('APP', 'num_tickets') if app_config['APP'].get('num_tickets') else 1,
            'footer' : app_config['APP']['footer'] if app_config['APP'].get('footer') else '',

        }
        
        return data