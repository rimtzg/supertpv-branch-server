from flask import Flask, render_template, g, session
from flask_httpauth import HTTPBasicAuth
import datetime
import threading
from time import sleep
import logging

from config import app_config
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

def get_updated_products():
    with app.app_context():
        while True:
            Sync().get_updated_products()
            sleep(int(app_config['API']['DELAY']))

@app.before_first_request
def first_start():
    Sync().get_all_products()

    thread = threading.Thread(target=get_updated_products)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=DEBUG )
