from schema import Schema, Optional, Use
from datetime import datetime

from bson import ObjectId

schema = Schema({
    '_id' : Use(ObjectId),
    'code' : Use(str.lower),
    'name' : Use(str.lower),
    Optional('category', default=None) : Use(ObjectId),
    Optional('mark', default=None) : Use(ObjectId),
    'description' : Use(str.lower),
    Optional('presentation', default=None) : Use(ObjectId),
    'content' : Use(float),
    Optional('unit', default=None) : Use(ObjectId),
    'cost' : Use(float),
    Optional('profit', default=20) : Use(int),
    'price' : Use(float),

    Optional('iva', default=False) : Use(bool),
    Optional('ieps', default=False) : Use(bool),
    Optional('promotion', default='') : Use(str.lower),
    Optional('charge', default='') : Use(str.lower),
    Optional('scale', default=False) : Use(bool),
    Optional('active', default=True) : Use(bool),
    Optional('visible', default=True) : Use(bool),
    Optional('percent_points', default=0) : Use(int),
    Optional('points', default=0) : Use(int),
    Optional('stock_min', default=0) : Use(int),
    Optional('sale_min', default=0) : Use(float),
}, ignore_extra_keys=True)

modify_schema = Schema({
    'user' : str.lower,
    'date' : Use(datetime),
}, ignore_extra_keys=True)