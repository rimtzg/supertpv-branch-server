from schema import Schema, Optional, Use, Or
from datetime import datetime
from bson import ObjectId

Returns = Schema({
    'cashier'   : Use(ObjectId),
    'session'   : Use(ObjectId),
    'date'      : Use(datetime.fromisoformat),
    'total'     : Or(Use(float), None),
    'number'    : Use(int),
    'reason'    : Use(str.lower),
    'sale'      : Use(ObjectId),
    'ticket'    : Use(int),
    'products'  : [
        {
            '_id'       : Use(ObjectId),
            'code'      : Use(str.lower),
            'name'      : Use(str.lower),
            'cost'      : Or(Use(float), None),
            'price'     : Or(Use(float), None),
            'amount'    : Or(Use(float), None),
            'subtotal'  : Or(Use(float), None),
        }
    ]
}, ignore_extra_keys=True)