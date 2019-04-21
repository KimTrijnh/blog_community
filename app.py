from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager


app = Flask(__name__)

# set config here, already set SECRET_KEY, DATABASE_URL
app.config.from_object(Config)

# DATABSE CONNECT below
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import User, Post, Topic, Comment, Event, Like, subs, bookmarks, Category

# DATABASE CONNECT above
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# ROUTES HERE
@app.route('/')
@app.route('/home')
def home():
    hot_topics= db.session.query(Topic, db.func.count(subs.c.user_id).label('total')).join(subs).group_by(Topic.title).order_by(desc('total')).limit(3)

    newly_created_topics= db.session.query(Topic, db.func.count(subs.c.user_id).label('total')).join(subs).group_by(Topic.title).order_by(desc(Topic.created_at)).limit(3)

    return render_template('home.html', title='Home', hot_topics=hot_topics, newly_created_topics=newly_created_topics)

@app.route('/discovery')
def discovery():
    topics = db.session.query(Topic, db.func.count(subs.c.user_id).label('total')).join(subs).group_by(Topic.title).order_by(desc('total'))
    return render_template('discovery.html', title="Discovery", topics=topics)