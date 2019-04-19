from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

#set config here, already set SECRET_KEY, DATABASE_URL
app.config.from_object(Config)

#DATABSE CONNECT AND SETTING MIGRATE
db = SQLAlchemy(app)
migrate = Migrate(app, db)



###  ROUTES HERE
@app.route('/')
@app.route('/home')
def home():
    return 'hello'







#always put this at bottom
import models