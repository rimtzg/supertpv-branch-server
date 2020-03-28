from schema import Schema, Optional, Use

from bson import ObjectId

schema = Schema({
    'product' : Use(ObjectId),
    Optional('volume_discount') : Use(ObjectId)
}, ignore_extra_keys=True)