from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_moment import Moment
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager



app = Flask(__name__)
moment = Moment(app)

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
    u = User.query.filter_by(id=1).first()
    return u.username


@app.route('/login')
def login():
    return render_template('login.html')



@app.route('/create_post/<int:topic_id>', methods=['GET','POST'])
@app.route('/create_post', methods=['GET','POST'])

# @login_required
def create_post(topic_id=None):
    current_user = User.query.filter_by(id=1).first()
    if not current_user.is_authenticated:
        flash('please login to create post')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            user_id = current_user.id
            category = request.form['category']
            topic_id = topic_id
            if title and content and category:
                p = Post(title = title, content = content, user_id = user_id, category_id = int(category), topic_id=topic_id)
                db.session.add(p)
                db.session.commit()
                flash('your post is successfull pulished')
                return redirect(url_for('post', post_id= p.id))
            else:
                flash('please check your title/content/category')
    return render_template('create_post.html')


@app.route('/post/<int:post_id>', methods= ['GET','POST'])
def post(post_id=None):
    current_user.id=1
    p = Post.query.filter_by(id=post_id).first()
    author = p.owner
    category = p.category
    if p.topic:
        posts_in_topic = p.topic.posts.filter(Post.id != p.id).all()
    else:
        posts_in_topic = None
    if request.method == 'POST':
        comment = request.form['comment']
        create_comment(comment, current_user.id, post_id)
    comments = p.comments.all()
    comments.reverse()
    return render_template('post.html', post = p, author = author, category = category, comments = comments, posts_in_topic=posts_in_topic)


def create_comment(content, user_id, post_id):
    c = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(c)
    db.session.commit()




@app.route('/create_topic', methods=['GET','POST'])
def create_topic():
    current_user = User.query.filter_by(id=1).first()
    if not current_user.is_authenticated:
        flash('please login to create topic')
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            user_id = current_user.id
            category = request.form['category']

            if title and description and category:
                t = Topic(title = title, description = description, user_id = user_id, category_id = int(category))
                db.session.add(t)
                db.session.commit()
                flash('your topic is successfull created')
                return redirect(url_for('topic', topic_id= t.id))
            else:
                flash('please check your title/description/category')
    return render_template('create_topic.html')

@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    current_user.id=1
    t = Topic.query.filter_by(id=topic_id).first()
    author = t.owner.username
    category = Category.query.filter_by(id=t.category_id).first()
    return render_template('topic.html', topic = t, author = author, category=category)