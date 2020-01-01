import configparser
import os

if(os.environ.get('SNAP_COMMON')):
    SNAP_COMMON = os.environ['SNAP_USER_COMMON']
else:
    SNAP_COMMON = ''

app_config = configparser.ConfigParser()
app_config.read( os.path.join( SNAP_COMMON, 'app_config.ini' ) )

print(app_config['API']['URL'])