from app import db
from datetime import datetime
 
class User(db.Model):
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
    topic_members = db.relationship('Topic_member', backref='member', lazy='dynamic')
    bookmarks = db.relationship('Bookmark', backref='owner', lazy='dynamic')
    

class Post(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index=True, nullable=False)
    content = db.Column(db.Text, index=True, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    # like_number = db.Column(db.Integer, default=0)
    # comment_number = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('Like', backref='post', lazy='dynamic')
    bookmarks = db.relationship('Bookmark', backref='post', lazy='dynamic')



class Topic(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), index=True, nullable=False)
    description = db.Column(db.String(260), nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posts = db.relationship('Post', backref='topic', lazy='dynamic')
    topic_members = db.relationship('Topic_member', backref='topic', lazy='dynamic')


class Comment(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(400), index=True, nullable=False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow, server_default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reaction_id = db.Column(db.Integer, db.ForeignKey('reaction.id'))

class Like(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    

class Topic_member(db.Column):
    id= db.Column(db.Integer, primary_key = True)
    topic_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
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


# class Reaction(db.Model):
#     id= db.Column(db.Integer, primary_key = True)
#     icon_url = db.Column(db.String(200), nullable=False)


    







