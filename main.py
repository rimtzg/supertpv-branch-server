from flask import Flask, render_template, g, session
from flask_httpauth import HTTPBasicAuth
from flask_script import Manager
import datetime
import logging
from time import sleep
import threading

from config import app_config, save_config_file
from sync import Sync

from routes.config import app as config
from routes.admin import app as admin

########################################################################
#                                                                      #
#                               VARIABLES                              #
#                                                                      #
########################################################################

DEBUG = app_config['APP']['DEBUG']
SECRET_KEY = app_config['SERVER']['SECRET_KEY']

########################################################################
#                                                                      #
#                                 INIT                                 #
#                                                                      #
########################################################################

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SECRET_KEY'] = SECRET_KEY
manager = Manager(app)

logging.basicConfig(level=logging.DEBUG)

########################################################################
#                                                                      #
#                              BLUEPRINTS                              #
#                                                                      #
########################################################################

app.register_blueprint(config)
app.register_blueprint(admin)

########################################################################
#                                                                      #
#                             FIRST REQUEST                            #
#                                                                      #
########################################################################

sync = Sync()
# date = app_config['API']['LAST_UPDATED']
# print(date)
# print(datetime.datetime.utcnow())
# sync.get_products(date)

def get_data():
    sync.get_products()
    sync.get_volume_discount()
    pass

def get_updates():
    sleep(120)

    while True:
        date = app_config['API']['LAST_UPDATED']
        
        sync.get_products(date)
        sync.get_volume_discount()

        app_config['API']['LAST_UPDATED'] = str(datetime.datetime.utcnow())
        save_config_file()

        sleep(int(app_config['API']['DELAY']))

@app.before_first_request
def first_start():
    # Sync().get_products()
    thread = threading.Thread(target=get_data)
    thread.start()

    thread = threading.Thread(target=get_updates)
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
#manager.add_command('run_sync', Sync().get_updated_products())

if __name__ == '__main__':
    # Sync().get_products()

    # thread = threading.Thread(target=get_updated_products)
    # thread.start()
    
    app.run(host='0.0.0.0', port=3001, debug=DEBUG )
