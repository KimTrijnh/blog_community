from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager



app = Flask(__name__)

#set config here, already set SECRET_KEY, DATABASE_URL
app.config.from_object(Config)

## DATABSE CONNECT below
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import User, Post, Topic, Comment, Event, Like, subs, bookmarks, Category

## DATABASE CONNECT above
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

###  ROUTES HERE
@app.route('/')
@app.route('/home')
def home():
    u = User.query.filter_by(user_id=1).first()
    return u.username


@app.route('/login')
def login():
    return render_template('login.html')



# @app.route('/create_post', methods=('GET','POST'))
# # @login_required
# def create_post():
#     current_user = User.query.filter_by(id=1).first()
#     if not current_user.is_authenticated:
#         flash('please login to create post')
#         return redirect(url_for('login'))
#     else:
#         if request.method == 'POST':
#             title = request.form['title']
#             content = request.form['content']
#             user_id = 1
#             category = request.form['category']
#             topic_id = None
#             if title and content and category:
#                 p = Post(title = title, content = content, user_id = user_id, category_id = int(category), topic_id=topic_id)
#                 db.session.add(p)
#                 db.session.commit()
#                 flash('your post is successfull pulished')
#                 return redirect(url_for('post', post_id= p.id))
#             else:
#                 flash('please check your title/content/catagory')
#     return render_template('create_post.html')


# @app.route('/post/<int:post_id>')
# def post(post_id):
#     p = Post.query.filter_by(id=post_id).first()
#     author = User.query.filter_by(id=p.user_id).first()
#     category = Category.query.filter_by(id=p.category_id).first()
#     return render_template('post.html', post = p, author = author, category = category)