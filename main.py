from flask import Flask, url_for, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config

import hashlib
import os

app = Flask(__name__)
app.config.from_object(Config)  # applying all config to app
db = SQLAlchemy(app)


import models


@app.route('/')
def home():
    return render_template('home.html', page_title="Home")



@app.route('/login', methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST' and "name" in request.form:

        name = request.form['name']
        password = request.form['pass']

        name_check = models.User.query.filter_by(name=name).first()

        if name_check is not None:
            salt = name_check.salt
            key = name_check.key
            new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            if key == new_key:
                session['name'] = name
                return redirect(url_for("home"))
            else:
                status = "Wrong user name or password."
                return render_template('login.html', status=status)
        else:
            status = "Wrong user name or password."
            return render_template('login.html', status=status)
    else:
        return render_template('login.html', page_title="Login")



@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up_post():
    if request.method == 'POST' and "sign_name" in request.form:
        name = request.form['sign_name']
        password = request.form['sign_pass']

        name_check = models.User.query.filter_by(name=name).first()

        if name_check is None:
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

            user = models.User(name=name, salt=salt, key=key)
            db.session.add(user)
            db.session.commit()
            session['name'] = name
            return redirect(url_for("home"))
        else:
            status = "Name Already Taken"
            return render_template('sign.html', page_title="Sign_up",status= status)
    else:
        return render_template('sign.html', page_title="Sign_up")



@app.route('/forgot')
def forgot():

    return render_template('forgot.html', page_title="forgot")


@app.route('/map')
def map():

    return render_template('map.html', page_title="map")


@app.route('/history')
def history():
    return render_template('history.html', page_title="history")


@app.route('/famous')
def famous():

    return render_template('famous.html', page_title="famous")


if __name__ == "__main__":
    app.run(debug=True)
