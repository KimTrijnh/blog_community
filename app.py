from flask import Flask, render_template, redirect, url_for, flash, request, session 
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
    return 'huong'


@app.route('/sign_up')
def register():
    if request.method=='POST':
        username = request.form ['username']
        password = request.form ['password']
        email = request.form ['email']
        db=get_db()
        error = None 
         

        if not username:
            error='Username is required.'
        elif db.execute('SELECT id from User WHERE username = ?', (username,)).fetchone() is not None: 
            error='This username is not available'
        elif not password:
            error='Password is required.'
        elif not email:
            error= 'Email is required.'
        elif  '@' not in email:
            error='Email must contain @.'
        elif db.execute('SELECT id from User WHERE email = ?', (email,)).fetchone() is not None: 
            error='This email has been registered.'
        
        if error is None:
            db.execute('INSERT INTO User (username,password,email) VALUES (?,?,?)', (username, generate_password_hash(password)), email))
            db.commit()
            return redirect(url_for('login.html'))
    flash(error)
    return render_template('sign_up.html')

@app.route('/login')
def login():
     if request.method=='POST':
        username = request.form ['username']
        password = request.form ['password']
        db=get_db()
        error = None 

        if not username:
            error='Username is required.'
        elif db.execute('SELECT id from User WHERE username = ?', (username,)).fetchone() is None: 
            error='This username is not registered!'
        elif not password:
            error='Password is required.'
        elif not check_password_hash((db.execute('SELECT id from User WHERE username = ?', (username,)).fetchone()['password']): 
            error='Incorrect Password!'

        if error is None: 
            session.clear()
            session['user_id']=db.execute('SELECT id from User WHERE username = ?', (username,)).fetchone().id
            return redirect(url_for('home'))
     flash(error)
     return render_template('login.html')

@app.before_app_request 
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None: 
        g.user = None 
    else 
        g.user = get_db().execute('SELECT * from User WHERE id =?',user_id).fetchone()

@app.route(/logout)
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route(/user_account)
def user_account(): 
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
        error= 'You have to login to access user_account page!'
    else
        user =  get_db().execute('SELECT * FROM User WHERE id=?',user_id).fetchone()
        bookmarks = get_db.execute('SELECT * FROM Bookmark WHERE user_id=?',user_id).fetchall()
        topics = get_db.execute('SELECT * FROM Topic WHERE user_id=?',user_id).fetchall()
        return render_template('user_account.html', user=user, bookmarks=bookmarks, topics=topics )

db.create_all()   
















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