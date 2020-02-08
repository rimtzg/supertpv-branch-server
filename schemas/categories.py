from schema import Schema, Optional, Use

from bson import ObjectId

schema = Schema({
    '_id' : Use(ObjectId),
    'name' : Use(str.lower),
    'product' : Use(str.lower),
    Optional('active', default=False) : bool,
}, ignore_extra_keys=True)