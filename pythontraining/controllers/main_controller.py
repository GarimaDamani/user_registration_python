import re
import logging
import hashlib
from flask import render_template, request, session, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy_utils import database_exists
from ..app import app
from ..config import application as ap
from ..models.models import User, db


@app.route('/')
def home():
    logging.info('Home page')
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            return handle_register_post()
        else:
            return render_template('user_register.html')
    except IntegrityError as error:
        logging.error(error)
        db.session().rollback()
        message = 'Sorry! either ' + request.form['username'] + ' or ' + request.form['email'] + ' is already taken. '
        message += 'Please make sure username and email are UNIQUE'
        flash(message)
        return render_template('user_register.html')
    except SQLAlchemyError as error:
        logging.error(error)
        db.session.rollback()
        message = 'Oops!! Something went wrong.'
        return render_template('display_message.html', msg=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if 'username' in session:
            message = 'Hey, ' + session['username']
            return render_template('display_message.html', msg=message)
        elif request.method == 'POST':
            return handle_login_post()
        else:
            return render_template('user_login.html')
    except Exception as error:
        logging.error(error)
        message = 'Oops!! Something went wrong.'
        return render_template('display_message.html', msg=message)


@app.route('/user', methods=['GET'])
def user():
    try:
        if 'username' in session:
            user_data_list = User.query.all()
            data = User.query.filter_by(username=session['username']).first()
            return render_template('user_data.html', value=data, user_list=user_data_list)
        else:
            flash('Please login in-order to continue')
            return redirect(url_for('login'))
    except SQLAlchemyError as error:
        logging.error(error)
        message = 'Oops!! Something went wrong.'
        return render_template('display_message.html', msg=message)


@app.route('/about')
def about():
    logging.info('About page')
    return render_template('about.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        message = 'You were logged out successfully!'
        return render_template('display_message.html', msg=message)
    else:
        flash('Please login in-order to continue')
        return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found():
    logging.info('Bad url request')
    message = 'Sorry, the URL you are looking for is not valid.'
    return render_template('display_message.html', msg=message), 404


@app.errorhandler(405)
def page_not_found():
    logging.info('Method not allowed')
    message = 'Sorry, some technical glitch happened here. Please contact Garima Damani'
    return render_template('display_message.html', msg=message), 405


def create_db():
    try:
        if database_exists(ap.database_name):
            logging.info('Database %s exists', ap.database_name)
        else:
            db.create_all()
            db.session.commit()
            logging.info('Database %s created successfully', ap.database_name)
    except SQLAlchemyError as error:
        logging.error(error)


def handle_register_post():
    username = request.form['username']
    password = (hashlib.md5(request.form['password'].encode())).hexdigest()
    phone = request.form['phone']
    if re.search(ap.regex_email, request.form['email']):
        email = request.form['email']
    else:
        message = 'Please make sure it is a valid email address'
        flash(message)
        return render_template('user_register.html')
    if len(request.form['phone']) != 10:
        message = 'Please make sure phone number is 10 digit'
        flash(message)
        return render_template('user_register.html')
    new_user = User(username=username, password=password, email=email, phone=phone)
    db.session.add(new_user)
    db.session.commit()
    message = 'Thank you! ' + username + ' for registering with Python Training Classes'
    return render_template('display_message.html', msg=message)


def handle_login_post():
    username = request.form['username']
    password = (hashlib.md5(request.form['password'].encode())).hexdigest()
    data = User.query.filter_by(username=username).first()
    if data is not None and data.username == username and data.password == password:
        session['username'] = data.username
        return redirect(url_for('user'))
    else:
        flash('Please check username or password')
        return render_template('user_login.html')
