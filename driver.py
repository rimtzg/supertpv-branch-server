from pymongo import MongoClient
from config import app_config

#mongo = PyMongo()
DB_URL = app_config['DATABASE']['URL']
if not(len(DB_URL)):
    DB_URL = 'localhost'

DB_PORT = app_config['DATABASE']['PORT']
if not(len(DB_PORT)):
    DB_PORT = '27017'

DB_USERNAME = app_config['DATABASE']['USERNAME']
DB_PASSWORD = app_config['DATABASE']['PASSWORD']
if not(len(app_config['DATABASE']['PASSWORD'])):
    DB_USERNAME = None
    DB_PASSWORD = None

DB_NAME = app_config['DATABASE']['NAME']
if not(len(DB_NAME)):
    DB_NAME = 'supertpv'

mongo = MongoClient(host=DB_URL, port=int(DB_PORT), username=DB_USERNAME, password=DB_PASSWORD)[DB_NAME]