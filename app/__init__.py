from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://ff:LaajC4KL80CWhu4J@richusx.me/sportsleague'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = '+Rc\Wum[ETM3:-<3"VEBpW$.mv[3_vD*u@>*GyMm)M8e4xt27v'

from app import views
