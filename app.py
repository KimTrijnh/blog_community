from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

#set config here, already set SECRET_KEY, DATABASE_URL
app.config.from_object(Config)

## DATABSE CONNECT below
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import User, Post, Topic, Comment, Event, Bookmark, Like, Topic_member, Category

## DATABASE CONNECT above


###  ROUTES HERE
@app.route('/')
@app.route('/home')
def home():
    u = User.query.filter_by(id=1).first()
    return u.username

