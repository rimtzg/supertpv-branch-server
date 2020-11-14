from schema import Schema, Optional, Use
from datetime import datetime
from bson import ObjectId

schema = Schema({
    '_id'             : Use(ObjectId),
    'initial_money'   : Use(float),
    'total_sales'     : Use(float),
    'num_of_sales'    : Use(int),
    'total_incomes'   : Use(float),
    'total_expenses'  : Use(float),
    'total_deposits'  : Use(float),
    'total_returns'   : Use(float),

    'start_date'      : Use(datetime),
    'end_date'        : Use(datetime),

    #'branch'          : Use(ObjectId),
    'cashier'         : Use(ObjectId),

}, ignore_extra_keys=True)