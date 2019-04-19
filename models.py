from app import db
from datetime import datetime
from flask_login import UserMixin

# DATABASES HERE 
class User(UserMixin, db.Model):
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
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=True )
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
    topic_members = db.relationship('Topic_member', backref='topic')


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
    

class Topic_member(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
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

################    
#ROUTES HERE
# @app.route('/')
# @app.route('/home')
# def home():
#     return 'hello'

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/create_post', methods=('GET', 'POST'))
# # @login_required
# def createPost():
#     # if not current_user.is_authenticated:
#     #     flash='please login to create new post'
#     #     return redirect(url_for('login'))
#     # else:
#     if request.method == 'POST':
#         title = request.form['title']
#         category_id = request.form['category']
#         content = request.form['content']
#         # topic_id = 
#         if title and content and category_id:
#             create_post(title, content, int(category_id), topic_id=None)
#             return redirect(url_for('home'))
#         else:
#             flash('invalid input')

#     return render_template('create_post.html')

# def create_post(title, content, category_id, user_id = 1, topic_id=None):
#     p = Post(title=title, content=content, user_id=user_id, category_id=category_id, topic_id=topic_id)
#     db.session.add(p)
#     db.session.commit()


# #always put this at bottom
# @login_manager.user_loader
# def load_user(id):
#     return User.query.get(int(id))





