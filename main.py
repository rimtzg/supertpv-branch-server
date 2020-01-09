from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth

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
    Sync().get_products()
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
