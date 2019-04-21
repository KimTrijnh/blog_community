from flask import Flask, render_template, redirect, url_for, flash, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc
from datetime import datetime
from flask_moment import Moment
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user


app = Flask(__name__)
moment = Moment(app)

#set config here, already set SECRET_KEY, DATABASE_URL
app.config.from_object(Config)

## DATABSE CONNECT below
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import User, Post, Topic, Comment, Event, likes, subs, bookmarks, Category

## DATABASE CONNECT above
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

###  ROUTES HERE
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


# @app.route('/login')
# def login():
#     return render_template('login.html')


@app.route('/create_post/<int:topic_id>', methods=['GET','POST'])
@app.route('/create_post', methods=['GET','POST'])
@login_required
def create_post(topic_id=None):
    # current_user = User.query.filter_by(id=1).first()
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
                return redirect(url_for('post', post_id= p.id))
            else:
                flash('please check your title/content/category')
    return render_template('create_post.html')


@app.route('/post/<int:post_id>', methods= ['GET','POST'])
def post(post_id=None):
    post = Post.query.filter_by(id=post_id).first()
    author = post.owner
    category = post.category
    icon_color = 'text-dark'
    like_color = 'text-dark'
    if post.topic:
        posts_in_topic = post.topic.posts.filter(Post.id != post.id).all()
    else:
        posts_in_topic = None
    if current_user.is_authenticated:
        if checkBookmarked(post, current_user):
            icon_color = 'text-primary'
        else:
            icon_color = 'text-dark'
        if checkLike(post, current_user):
            like_color = 'text-danger'
        else:
            like_color = 'text-dark'
    if request.method == 'POST':
        comment = request.form['comment']
        create_comment(comment, current_user.id, post_id)
    comments = post.comments.all()
    comment_total = len(post.comments.all())
    bookmark_total = len(post.bookmarkers.all())
    like_total = len(post.likes.all())
    comments.reverse()
    return render_template('post.html', post = post, author = author, category = category, comments = comments, posts_in_topic=posts_in_topic, icon_color = icon_color, like_color=like_color, comment_total=comment_total, bookmark_total=bookmark_total, like_total = like_total)


def create_comment(content, user_id, post_id):
    c = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(c)
    db.session.commit()



@app.route('/create_topic', methods=['GET','POST'])
@login_required
def create_topic():
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
                topic = Topic(title = title, description = description, user_id = user_id, category_id = int(category))
                db.session.add(topic)
                topic.subscribers.append(current_user)
                db.session.commit()
                return redirect(url_for('topic', topic_id= topic.id))
            else:
                flash('please check your title/description/category')
    return render_template('create_topic.html')


@app.route('/topic/<int:topic_id>')
def topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    author = topic.owner.username
    category = Category.query.filter_by(id=topic.category_id).first()
    return render_template('topic.html', topic = topic, author = author, category=category)


# bookmarking
def isBookmarked(post, user):
    post.bookmarkers.append(user)
    db.session.commit()

def unBookmarked(post, user):
    post.bookmarkers.remove(user)
    db.session.commit()

@app.route('/clickbtn/<int:post_id>', methods=['GET','POST'])
@login_required
def clicked(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if checkBookmarked(post, current_user):
        unBookmarked(post, current_user)
    else:
        isBookmarked(post, current_user)
    return redirect(url_for('post', post_id= post_id))

def checkBookmarked(post, user):
    user = post.bookmarkers.filter_by(id = user.id).first()
    if user:
        return True
    else:
        return False

# liking
def checkLike(post, user):
    user = post.likes.filter_by(id = user.id).first()
    if user:
        return True
    else:
        return False

def isLiked(post, user):
    post.likes.append(user)
    db.session.commit()

def unLiked(post, user):
    post.likes.remove(user)
    db.session.commit()

@app.route('/toggleLike/<int:post_id>', methods=['GET','POST'])
@login_required
def toggleLike(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if checkLike(post, current_user):
        unLiked(post, current_user)
    else:
        isLiked(post, current_user)
    return redirect(url_for('post', post_id= post_id))



## OANH

@app.route('/sign_up', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username = request.form ['username']
        password = request.form ['password']
        email = request.form ['email']
        error = None 
        user = User.query.filter_by(username = username).first()
        check_email  = User.query.filter_by(email = email).first()
        if not username:
            error='Username is required.'
        elif user is not None: 
            error='This username is not available'
        elif not password:
            error='Password is required.'
        elif not email:
            error= 'Email is required.'
        elif  '@' not in email:
            error='Email must contain @.'
        elif check_email is not None: 
            error='This email has been registered.'
        else:
            user = User(username = username, email = email, password_hash = password)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home'))
        flash(error)
    return render_template('signup.html')
            


@app.route('/login', methods=['GET', 'POST'])
def login():
     if request.method=='POST':
        username = request.form ['username']
        password = request.form ['password']
        error = None 
        user = User.query.filter_by(username = username).first()
        if not username:
            error='Username is required.'
            flash(error, 'danger')
        elif user is None: 
            error='This username is not registered!'
            flash(error, 'danger')
        elif not password:
            error='Password is required.'
            flash(error, 'danger')
        elif not user.check_password(password): 
            error='Incorrect Password!'
            flash(error, 'danger')
            return redirect(url_for('login'))
        else:
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                return redirect(url_for('home'))  
            return redirect(next_page)

     return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



# @app.before_app_request 
# def load_logged_in_user():
#     user_id = session.get('user_id')
#     if user_id is None: 
#         g.user = None 
#     else:
#         g.user = get_db().execute('SELECT * from User WHERE id =?',user_id).fetchone()


# @app.route('/user_account')
# def user_account():
#     user_id = session.get('user_id')
#     if user_id is None:
#         return redirect(url_for('login.html'))
#         error= 'You have to login to access user_account page!'
#     else:
#         user =  get_db().execute('SELECT * FROM User WHERE id=?',user_id).fetchone()
#         bookmarks = get_db.execute('SELECT * FROM Bookmark WHERE user_id=?',user_id).fetchall()
#         topics = get_db.execute('SELECT * FROM Topic WHERE user_id=?',user_id).fetchall()
#         return render_template('user_account.html', user=user, bookmarks=bookmarks, topics=topics )


