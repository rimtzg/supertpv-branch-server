from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from config import app_config

PREFIX = 'admin'

app = Blueprint(PREFIX, __name__, url_prefix='/'+PREFIX)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app_config['SERVER']['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app_config['SERVER']['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))