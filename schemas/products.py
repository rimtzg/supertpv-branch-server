from schema import Schema, Optional, Use
from datetime import datetime

from bson import ObjectId

schema = Schema({
    'code' : Use(str.lower),
    Optional('name') : Use(str.lower),
    Optional('category', default=None) : Use(ObjectId),
    Optional('mark', default=None) : Use(ObjectId),
    Optional('description') : Use(str.lower),
    Optional('presentation', default=None) : Use(ObjectId),
    Optional('content') : Use(str),
    Optional('unit', default=None) : Use(ObjectId),
    'cost' : Use(float),
    Optional('profit', default=20) : Use(int),
    'price' : Use(float),

    Optional('round', default=True) : Use(bool),
    Optional('pin',   default=False) : Use(bool),

    Optional('iva', default=False) : Use(bool),
    Optional('ieps', default=False) : Use(bool),
    Optional('volume_discount', default=None) : Use(ObjectId),
    #Optional('charge', default=None) : Use(ObjectId),
    Optional('scale', default=False) : Use(bool),
    Optional('active', default=True) : Use(bool),
    Optional('visible', default=True) : Use(bool),
    Optional('percent_points', default=0) : Use(int),
    Optional('points', default=0) : Use(int),
    Optional('stock_min', default=0) : Use(int),
    Optional('sale_min', default=0) : Use(float),

    #'modified' : Use(datetime),
}, ignore_extra_keys=True)

modifications = Schema({
    'cost' : Use(float),
    Optional('profit', default=20) : Use(int),
    'price' : Use(float),
    Optional('volume_discount', default=None) : Use(ObjectId),
    #Optional('charge', default=None) : Use(ObjectId),
    Optional('scale', default=False) : Use(bool),
    Optional('active', default=True) : Use(bool),
    Optional('visible', default=True) : Use(bool),
    Optional('percent_points', default=0) : Use(int),
    Optional('points', default=0) : Use(int),
    Optional('stock_min', default=0) : Use(int),
    Optional('sale_min', default=0) : Use(float),

    #'modified' : Use(datetime),
}, ignore_extra_keys=True)

modify_schema = Schema({
    'user' : str.lower,
    'date' : Use(datetime),
}, ignore_extra_keys=True)