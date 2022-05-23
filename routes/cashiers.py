from flask import Blueprint, render_template, session, request, abort, flash, redirect, url_for
from methods import Cashiers

PREFIX = 'cashiers'

app = Blueprint(PREFIX, __name__, url_prefix='/cashiers')

@app.route('/', methods=['GET'])
#@parse_token
def home():
    data = {
        'cashiers' : Cashiers().list()
    }
    
    return render_template('cashiers/list.html', **data)

@app.route('/new', methods=['GET'])
def new():
    document = {}

    return render_template('cashiers/edit.html', document=document)

@app.route('/edit/<_id>', methods=['GET'])
def edit(_id):
    data = {
        'document' : Cashiers().get(_id)
    }

    return render_template('cashiers/edit.html', **data)

@app.route('/save', methods=['POST'])
def save():
    data = request.form.to_dict()

    if(data.get('_id')):
        document = Cashiers().update(data['_id'], data)
    else:
        document = Cashiers().insert(data)

    if(document):
        flash('Cajero guardado')
    else:
        flash('No se guardo el cajero')
    
    return redirect( url_for('cashiers.home') )

@app.route('/delete/<_id>', methods=['GET'])
def delete(_id):
    is_ok = Cashiers().delete(_id)

    if(is_ok):
        flash('Cajero eliminado')
    else:
        flash('No se elimino el cajero')

    return redirect( url_for('cashiers.home') )

