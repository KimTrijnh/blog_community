from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

#set config here
app.config.from_object(Config)

#connect to database
db = SQLAlchemy(app)


#routes here
@app.route('/')
@app.route('/home')
def home():
    return 'hello'
