from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# DATABASES HERE


subs = db.Table('subs', 
db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
db.Column('topic_id', db.Integer, db.ForeignKey('topic.id')))

bookmarks = db.Table('bookmarks', 
db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
db.Column('user.id', db.Integer, db.ForeignKey('user.id')))


class User(UserMixin, db.Model, object):
    id= db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120), nullable=False)
    posts = db.relationship('Post', backref='owner', lazy='dynamic')
    likes = db.relationship('Like', backref='owner', lazy='dynamic')
    posts= db.relationship('Post', backref='owner', lazy='dynamic')
    topics = db.relationship('Topic', backref='owner', lazy='dynamic')
    comments = db.relationship('Comment', backref='owner', lazy='dynamic')
    likes = db.relationship('Like', backref='owner', lazy='dynamic')
    events = db.relationship('Event', backref='owner', lazy='dynamic')
    subscriptions = db.relationship('Topic', secondary='subs', backref=db.backref('subscribers', lazy='dynamic'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Topic(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('Post', backref='topic', lazy='dynamic')



class Post(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index=True, nullable=False)
    content = db.Column(db.Text, index=True, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True )
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('Like', backref='post', lazy='dynamic')
    bookmarks = db.relationship('User', secondary='bookmarks', backref=db.backref('posts', lazy='dynamic'))




class Comment(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(400), index=True, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    # reaction_id = db.Column(db.Integer, db.ForeignKey('reaction.id'))

class Like(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    


class Category(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), index=True, nullable=False)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

class Event(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    



class Bookmark(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# class Topic_member(db.Model):
#     id= db.Column(db.Integer, primary_key = True)
#     topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

## FUNCTIONS TO ADJUST DATABASE TABLE'S
# db.create_all()
def create_category(name):
    c = Category(name=name)
    db.session.add(c)
    db.session.commit()

# create_category('Frontend Development')
# create_category('Backend Development')
# create_category('Design UI/UX')

def del_row_category(id):
    c = Category.query.filter_by(id=id).first()
    db.session.delete(c)
    db.session.commit()








