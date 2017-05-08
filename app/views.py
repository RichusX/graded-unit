from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import auth
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

def setSessionVariables():
    if 'subscription' not in session:
        session['subscription'] = 0
    if 'junior' not in session:
        session['junior'] = False

def resetSessionVariables():
    session['logged_in'] = False
    session['subscription'] = 0
    session['junior'] = False

@app.route('/')
@app.route('/index')
def index(): # Index page (Homepage)
    setSessionVariables()
    if not session.get('logged_in'):
        return render_template('index.html')
    else:
        if request.method == 'POST':
            username = getname(request.form['username'])
            return render_template('index.html')
    return render_template('index.html')

@app.route('/tables')
def tables(): # Championship Table page
    setSessionVariables()
    return render_template('tables.html')

@app.route('/players')
def players(): # Player Info Page
    setSessionVariables()
    info = Player.query.all()
    return render_template('players.html', data=info)

@app.route('/login', methods=['GET', 'POST'])
def login(): # Login Page
    setSessionVariables()
    if request.method == 'GET':
        return render_template('login.html')
    else:
        try: # Try to retreive password hash
            username = request.form['username']
            user = User.query.filter_by(username = username).first()
            print (user.password)
            if auth.check_pw(request.form['password'], user.password): # If login is successful, set session variables and forward user to homepage
                session['logged_in'] = True
                session['subscription'] = user.subscription
                if user.junior == "True":
                    session['junior'] = True
                else:
                    session['junior'] = False
                return render_template('index.html', data="Login Successful!")
            else: # If login has failed then forward user back to login page with an error message displayed.
                return render_template('login.html', data="Login Failed. Please try again!")
        except: # If fails to retreive password hash, display error message.
            return render_template('login.html', data="Critical error. Please contact the webmaster at me@richusx.me")

@app.route('/register', methods=['GET', 'POST'])
def register(): # Register Page
    setSessionVariables()
    if request.method == 'POST':
        data = User.query.filter_by(username = request.form['username']).first()
        if data is None:
            pw_hash = auth.salt_pw(request.form['password'])
            try: # If junior checkbox is not ticked then write to db junior = False
                junior = request.form['junior']
                if junior is not None:
                    new_user = User(fullname = request.form['fullname'], email = request.form['email'], username = request.form['username'], password = pw_hash, subscription = request.form['subscription'], junior = "True")
            except: # Else write to db that junior = True
                new_user = User(fullname = request.form['fullname'], email = request.form['email'], username = request.form['username'], password = pw_hash, subscription = request.form['subscription'], junior = "False")
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        else:
            return render_template('register.html', data="Username already taken. Please choose a different one.")
    return render_template('register.html')

@app.route('/logout')
def logout(): # Reset session variables and forward user to homepage
    resetSessionVariables()
    return redirect('/')
