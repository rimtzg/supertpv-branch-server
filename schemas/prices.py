from schema import Schema, Optional, Use

from bson import ObjectId

schema = Schema({
    'product' : Use(ObjectId),
    'cost' : Use(float),
    'profit' : Use(int),
    'price' : Use(float),

    Optional('round', default=True) : Use(bool),
    Optional('pin',   default=False) : Use(bool),

    Optional('percent_points', default=0) : Use(int),
    Optional('points', default=0) : Use(int),
}, ignore_extra_keys=True)