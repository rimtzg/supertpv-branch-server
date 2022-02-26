from flask import Flask, render_template, g, session
from flask_httpauth import HTTPBasicAuth
# from flask_script import Manager
from flask_cors import CORS
from datetime import date, datetime
import logging
from time import sleep
import threading
import json
from bson import ObjectId

from config import app_config, save_config_file

from routes.config import app as config
from routes.admin import app as admin
from routes.api import app as api

########################################################################
#                                                                      #
#                               VARIABLES                              #
#                                                                      #
########################################################################

try:
    DEBUG = app_config['APP']['DEBUG']
except:
    DEBUG = True
SECRET_KEY = app_config['SERVER']['SECRET_KEY']

########################################################################
#                                                                      #
#                                 INIT                                 #
#                                                                      #
########################################################################

app = Flask(__name__)
cors = CORS(app)
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = SECRET_KEY
# manager = Manager(app)

logging.basicConfig(level=logging.DEBUG)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

app.json_encoder = JSONEncoder

########################################################################
#                                                                      #
#                              BLUEPRINTS                              #
#                                                                      #
########################################################################

app.register_blueprint(config)
app.register_blueprint(admin)
app.register_blueprint(api)

########################################################################
#                                                                      #
#                             FIRST REQUEST                            #
#                                                                      #
########################################################################

    #     # UPLOAD #
    #     sync.upload_closed_sessions()
    #     sync.upload_actual_session()
    #     sync.upload_sales()
    #     sync.upload_old_sessions()
    #     sync.upload_old_actual_session()
    #     sync.upload_old_sales()
    #     sync.upload_recharges()

    #     DATE = NEW_DATE
    #     #save_config_file()

    #     sleep(DELAY_TIME)

from syncs import sync_cashiers
from syncs import sync_products
from syncs import sync_volume_discounts
from syncs import sync_recharges
from syncs import sync_sessions

@app.before_first_request
def first_start():
    thread = threading.Thread(target=sync_cashiers)
    thread.start()

    thread = threading.Thread(target=sync_products)
    thread.start()

    thread = threading.Thread(target=sync_volume_discounts)
    thread.start()

    thread = threading.Thread(target=sync_recharges)
    thread.start()

    thread = threading.Thread(target=sync_sessions)
    thread.start()

    pass

########################################################################
#                                                                      #
#                                 HOME                                 #
#                                                                      #
########################################################################

@app.route('/')
def home():
    return render_template('index.html')

########################################################################
#                                                                      #
#                                 START                                #
#                                                                      #
########################################################################

# def get_updated_products():
#     while True:
#         date = app_config['API']['LAST_UPDATED']
#         Sync().get_products(date)
        
#         sleep(int(app_config['API']['DELAY']))

#manager.add_command('run_get', Sync().get_products())
# manager.add_command('run_sync', on_starting)

if __name__ == '__main__':
    # sync = Sync()

    # get_data()

    # thread = threading.Thread(target=get_updates)
    # thread.start()
    
    app.run(host='0.0.0.0', port=8000, debug=DEBUG )
    # manager.run()
