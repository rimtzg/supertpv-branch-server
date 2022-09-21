from flask import Blueprint, render_template, session, request, abort, flash, redirect, url_for
from config import app_config, save_config_file

from sync import Sync

PREFIX = 'config'

app = Blueprint(PREFIX, __name__, url_prefix='/'+PREFIX)

@app.route('/', methods=['GET'])
#@parse_token
def home():
    return render_template('config.html', config=app_config)

@app.route('/save', methods=['POST'])
def save():
    if not session.get('logged_in'):
        abort(401)

    app_config['API']['URL']            = request.form['api_url']
    app_config['API']['TOKEN']          = request.form['api_token']
    # app_config['API']['USERNAME']       = request.form['api_username']
    # app_config['API']['PASSWORD']       = request.form['api_password']
    # app_config['API']['BUSINESS']       = request.form['api_business']
    # app_config['API']['BRANCH']         = request.form['api_branch']
    app_config['API']['DELAY']          = request.form['api_delay']

    app_config['SERVER']['USERNAME']    = request.form['server_username']
    app_config['SERVER']['PASSWORD']    = request.form['server_password']
    app_config['SERVER']['SECRET_KEY']  = request.form['server_secret_key']

    app_config['APP']['DEBUG']          = request.form['app_debug']

    app_config['DATABASE']['URL']       = request.form['db_url']
    app_config['DATABASE']['NAME']       = request.form['db_name']
    app_config['DATABASE']['PORT']      = request.form['db_port']
    app_config['DATABASE']['USERNAME']  = request.form['db_username']
    app_config['DATABASE']['PASSWORD']  = request.form['db_password']

    save_config_file()

    flash('Configuration was successfully saved')
    return redirect(url_for('home'))

@app.route('/sync', methods=['POST'])
def sync():
    if not session.get('logged_in'):
        abort(401)
        
    sync = Sync()
    sync.del_products()
    sync.get_all_products()

    flash('Synchronized products')
    return redirect(url_for('index.home'))

