from pymongo import MongoClient
from config import app_config

#mongo = PyMongo()
DB_URL = app_config['DATABASE']['URL']
DB_PORT = app_config['DATABASE']['PORT']
if(len(app_config['DATABASE']['PASSWORD'])):
    DB_USERNAME = app_config['DATABASE']['USERNAME']
    DB_PASSWORD = app_config['DATABASE']['PASSWORD']
else:
    DB_USERNAME = None
    DB_PASSWORD = None
DB_NAME = app_config['DATABASE']['NAME']

mongo = MongoClient(host=DB_URL, port=int(DB_PORT), username=DB_USERNAME, password=DB_PASSWORD)[DB_NAME]