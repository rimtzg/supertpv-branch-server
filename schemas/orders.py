from schema import Schema, Optional, Use, Or
from datetime import datetime

from bson import ObjectId

# from order_templates import schema as order_template

schema = Schema({
    '_id'           : Use(ObjectId),
    'client_id'     : Use(ObjectId),
    'client_name'   : Use(str.lower),
    Optional('date') : Use(datetime.fromisoformat),
    'number'        : Use(int),
    Optional('active', default=True) : Use(bool),
    
    'categories' : [
        {
            '_id'      : Use(ObjectId),
            'name'     : Use(str.lower),
            'products' : [
                {
                    '_id'    : Use(ObjectId),
                    'code'   : Use(str.lower),
                    'name'   : Use(str.lower),
                    'amount' : Or(Use(int), Use(float)),
                    'label'  : Use(str.lower),
                    'price'  : Or(Use(int), Use(float))
                }
            ]
        }
    ]

}, ignore_extra_keys=True)