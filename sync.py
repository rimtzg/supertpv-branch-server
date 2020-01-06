import configparser
import os

if(os.environ.get('SNAP_COMMON')):
    SNAP_COMMON = os.environ['SNAP_COMMON']
else:
    SNAP_COMMON = ''

app_config = configparser.ConfigParser()
app_config.read( os.path.join( SNAP_COMMON, 'app_config.ini' ) )

ACCOUNT = app_config['API']['ACCOUNT']
USERNAME = app_config['API']['USERNAME']
PASSWORD = app_config['API']['PASSWORD']

