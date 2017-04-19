from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_recaptcha import ReCaptcha
from app import app

recaptcha = ReCaptcha(app=app, )

db = SQLAlchemy(app)


class User(db.Model):
    """ Create user table """
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    subscription = db.Column(db.Integer)
    junior = db.Column(db.String(5))


    def __init__(self, fullname, email, username, password, subscription, junior):
        self.fullname = fullname
        self.email = email
        self.username = username
        self.password = password
        self.subscription = int(subscription)
        self.junior = junior


@app.route('/')
@app.route('/index')
def index():
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html')
    return render_template('index.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        try:
            data = User.query.filter_by(username = username, password = password).first()
            if data is not None:
                session['logged_in'] = True
                return render_template('index.html', data="Login Successful!")
            else:
                return render_template('login.html', data="Login Failed. Please try again!")  #redirect(url_for('login'), data = "Login Failed. Please try again!")
        except:
            return render_template('login.html', data="Critical error. Please contact the webmaster at me@richusx.me")#redirect(url_for('login'), data = "Critical error. Please contact the webmaster at me@richusx.me")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register Form"""
    if request.method == 'POST':
        if recaptcha.verify():
            data = User.query.filter_by(username = request.form['username']).first()
            if data is None:
                new_user = User(fullname = request.form['fullname'], email = request.form['email'], username = request.form['username'], password = request.form['password'], subscription = request.form['subscription'], junior = request.form['junior'])
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')
            else:
                return render_template('register.html', data="Username already taken. Please choose a different one.")
        else:
            return render_template('register.html', data="ReCaptcha invalid.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout Form"""
    session['logged_in'] = False
    return redirect('/')
