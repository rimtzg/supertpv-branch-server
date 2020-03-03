from schema import Schema, Optional, Use
from datetime import datetime

from bson import ObjectId

schema = Schema({
    'name' : Use(str.lower),
    'amount' : Use(int),
    'discount' : Use(float),
    'from' : Use(bool),
    'active' : Use(bool),
}, ignore_extra_keys=True)

modifications = Schema({
    'amount' : Use(int),
    'discount' : Use(float),
    'from' : Use(bool),
    'active' : Use(bool),
}, ignore_extra_keys=True)