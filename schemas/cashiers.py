from schema import Schema, Optional, Use

schema = Schema({
    'name' : Use(str.lower),
    'username' : Use(str.lower),
    'password' : Use(str.lower),
    Optional('active', default=False) : Use(bool),
}, ignore_extra_keys=True)