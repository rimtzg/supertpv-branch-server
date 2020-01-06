from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth

from config import app_config

from routes.config import app as config
from routes.admin import app as admin

########################################################################
#                                                                      #
#                               VARIABLES                              #
#                                                                      #
########################################################################

DEBUG = app_config['APP']['DEBUG']
SECRET_KEY = app_config['SERVER']['SECRET_KEY']

API_URL = app_config['API']['URL']
API_ACCOUNT = app_config['API']['ACCOUNT']
API_USERNAME = app_config['API']['USERNAME']
API_PASSWORD = app_config['API']['PASSWORD']

DB_URL = app_config['DATABASE']['URL']
DB_PORT = app_config['DATABASE']['PORT']
DB_USERNAME = app_config['DATABASE']['USERNAME']
DB_PASSWORD = app_config['DATABASE']['PASSWORD']

########################################################################
#                                                                      #
#                                 INIT                                 #
#                                                                      #
########################################################################

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = SECRET_KEY

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

@app.before_first_request
def first_start():
    #if not (os.path.isfile( app.conf['DATABASE'] )):
    #init_db()
    #start_sync()
    #start_sync()
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
