from schema import Schema, Optional, Use, Or

from bson import ObjectId

schema = Schema({
    Optional('stock', default=0) : Use(float),
    Optional('stock_min', default=0) : Use(float),
    Optional('sale_min', default=0) : Use(float),
}, ignore_extra_keys=True)