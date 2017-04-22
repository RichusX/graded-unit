from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    """ Create user table """
    id = db.Column(db.Integer, primary_key = True)
    fullname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    username = db.Column(db.String(64), unique = True)
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

class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key = True)
    number = db.Column(db.Integer)
    name = db.Column(db.String())
    dob = db.Column(db.String())
    info = db.Column(db.String())
    sponsor = db.Column(db.String())
    previousclub = db.Column(db.String())
    yearsigned = db.Column(db.Integer)
    position = db.Column(db.String())
    imageurl = db.Column(db.String())

    def __init__(self, id, number, name, dob, info, sponsor, previousclub, yearsigned, position, imageurl):
        self.id = id
        self.number = number
        self.name = name
        self.dob = dob
        self.info = info
        self.sponsor = sponsor
        self.previousclub = previousclub
        self.yearsigned = yearsigned
        self.position = position
        self.imageurl = imageurl

def fixSubscription():
    if "subscription" not in session:
        session["subscription"] = 0


@app.route('/')
@app.route('/index')
def index():
    fixSubscription()
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html')
    return render_template('index.html')

@app.route('/tables')
def tables():
    fixSubscription()
    return render_template('tables.html')

@app.route('/players')
def players():
    fixSubscription()
    info = Player.query.all()
    return render_template('players.html', data=info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    fixSubscription()
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        try:
            data = User.query.filter_by(username = username, password = password).first()
            print (data)
            if data is not None:
                session['logged_in'] = True
                session['subscription'] = data.subscription
                return render_template('index.html', data="Login Successful!")
            else:
                return render_template('login.html', data="Login Failed. Please try again!")  #redirect(url_for('login'), data = "Login Failed. Please try again!")
        except:
            return render_template('login.html', data="Critical error. Please contact the webmaster at me@richusx.me")#redirect(url_for('login'), data = "Critical error. Please contact the webmaster at me@richusx.me")

@app.route('/register', methods=['GET', 'POST'])
def register():
    fixSubscription()
    """Register Form"""
    if request.method == 'POST':
        data = User.query.filter_by(username = request.form['username']).first()
        if data is None:
            try:
                junior = request.form['junior']
                if junior is not None:
                    new_user = User(fullname = request.form['fullname'], email = request.form['email'], username = request.form['username'], password = request.form['password'], subscription = request.form['subscription'], junior = "False")
            except:
                new_user = User(fullname = request.form['fullname'], email = request.form['email'], username = request.form['username'], password = request.form['password'], subscription = request.form['subscription'], junior = request.form['junior'])
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        else:
            return render_template('register.html', data="Username already taken. Please choose a different one.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout Form"""
    session['logged_in'] = False
    session['subscription'] = 0
    return redirect('/')
