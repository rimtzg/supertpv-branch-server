from datetime import datetime

from flask import Blueprint, render_template, session, request, abort, flash, redirect, url_for
from methods import Api, Cashiers

PREFIX = 'index'

app = Blueprint(PREFIX, __name__, url_prefix='/')

@app.route('/', methods=['GET'])
#@parse_token
def home():
    start = datetime.utcnow().replace(hour=0, minute=0, second=0)
    end = datetime.utcnow().replace(hour=23, minute=59, second=59)

    products = Api().get_products_count()
    cashiers = Cashiers().count()
    discounts = Api().get_discounts_count()
    products_discounts = Api().get_products_with_discounts_count()
    num_sales = Api().get_num_sales(start, end)
    total_sales = Api().get_total_sales(start, end)

    data = {
        'products' : products,
        'cashiers' : cashiers,
        'discounts' : discounts,
        'products_discounts' : products_discounts,
        'num_sales' : num_sales,
        'total_sales' : total_sales,
    }

    return render_template('index.html', **data)