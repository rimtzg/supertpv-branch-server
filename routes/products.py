from flask import Blueprint, render_template, session, request, abort, flash, redirect, url_for
from methods import Products

PREFIX = 'products'

app = Blueprint(PREFIX, __name__, url_prefix='/products')

@app.route('/', methods=['GET'])
#@parse_token
def home():
    data = {
        'products' : Products().list()
    }
    
    return render_template('products/list.html', **data)

@app.route('/new', methods=['GET'])
def new():
    document = {}

    return render_template('products/edit.html', document=document)

@app.route('/edit/<_id>', methods=['GET'])
def edit(_id):
    data = {
        'document' : Products().get(_id)
    }

    return render_template('products/edit.html', **data)

@app.route('/save', methods=['POST'])
def save():
    data = request.form.to_dict()

    if(data.get('_id')):
        document = Products().update(data['_id'], data)
    else:
        document = Products().insert(data)

    if(document):
        flash('Producto guardado')
    else:
        flash('No se guardo el producto')
    
    return redirect( url_for('products.home') )

@app.route('/delete/<_id>', methods=['GET'])
def delete(_id):
    is_ok = Products().delete(_id)

    if(is_ok):
        flash('Producto eliminado')
    else:
        flash('No se elimino el producto')

    return redirect( url_for('products.home') )

