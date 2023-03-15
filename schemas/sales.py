from schema import Schema, Optional, Use, Or
from datetime import datetime
from bson import ObjectId

def str_to_float(text):
    if(len(text) > 0):
        if(text == '.'):
            return 0
            
    return 0

Sales = Schema({
    '_id'               : Use(ObjectId),
    'cashier_id'        : Use(ObjectId),
    'cashier_name'      : Use(str.lower),
    'session_id'        : Use(ObjectId),
    'date'              : Use(datetime.fromisoformat),
    'total'             : Or(Use(float), None),
    'cash'              : Or(Use(float), None),
    'change'            : Or(Use(float), None),
    'subtotal'          : Or(Use(float), None),
    'total_discounts'   : Or(Use(float), None),
    Optional('ticket')  : Or(Use(int), None),
    'num_of_products'   : Or(Use(int), None),
    
    Optional('canceled', default=False) : Use(bool),

    Optional('products') : [
        {
            '_id'       : Use(ObjectId),
            'code'      : Use(str.lower),
            'name'      : Use(str.lower),
            'cost'      : Or(Use(float), None),
            'price'     : Or(Use(float), None),
            'amount'    : Or(Use(float), Use(str_to_float), None),
            'subtotal'  : Or(Use(float), Use(str_to_float), None),
            Optional('returned', default=False) : Use(bool),
        }
    ],

    Optional('card') : [
        {
            'amount'        : Or(Use(float), Use(str_to_float), None),
            'total'         : Or(Use(float), None),
            'operation'     : Use(str),
            'commission'    : Or(Use(float), None),
            'percent'       : Or(Use(float), None),
        }
    ],

    Optional('discounts') : [
        {
            '_id'       : Use(ObjectId),
            'amount'    : Use(float),
            'count'     : Use(float),
            'discount'  : Use(float),
            'name'      : Use(str),
            'total'     : Use(float),
        }
    ],

    Optional('services') : [
        {
            'type'  : Use(str),
            'title' : Use(str),
            'total' : Use(float),
        }
    ],
}, ignore_extra_keys=True)