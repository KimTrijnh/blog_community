from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#set config here, already set SECRET_KEY, DATABASE_URL
app.config.from_object(Config)

#connect to database
db = SQLAlchemy(app)


#ROUTES HERE
@app.route('/')
@app.route('/home')
def home():
    return 'hello'


import models