from schema import Schema, Optional, Use, Or
from datetime import datetime
from bson import ObjectId

Orders = Schema({
    'branch_id'         : Use(ObjectId),
    'branch_name'       : Use(str.lower),

    'client_id'         : Use(ObjectId),
    'client_name'       : Use(str.lower),

    'date'              : Use(datetime.fromisoformat),
    'number'            : Or(Use(int), None),
    'total_products'    : Or(Use(int), None),

    'categories' : [
        {
            '_id'      : Use(ObjectId),
            'name'     : Use(str.lower),
            'num_of_products'   : Or(Use(int), None),
            'products' : [
                {
                    '_id'    : Use(ObjectId),
                    'code'   : Use(str.lower),
                    'name'   : Use(str.lower),
                    'amount' : Use(float),
                }
            ]
        }
    ],
}, ignore_extra_keys=True)