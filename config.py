import configparser
import os
from pathlib import Path

INI = 'app_config.ini'

if(os.environ.get('SNAP_COMMON')):
    DIRECTORY = os.environ['SNAP_COMMON']
else:
    DIRECTORY = str(Path.home())

FILE = os.path.join( DIRECTORY, INI )

# file = Path(FILE)
# if not(file.exists()):
#     os.popen('cp ' + INI + ' ' + FILE)

app_config = configparser.ConfigParser()
app_config.read( FILE )

app_config['FIX'] = {
    'CARD_PAYMENTS' : 'False'
}

def save_config_file():
    with open( FILE , 'w') as configfile:
        app_config.write(configfile)