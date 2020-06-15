import dotenv
import os

from flask import Flask
from flask import request
from flask import Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./esperanzo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all() #initialize the db if it doesn't already exists

from esperanzo_bot import routes # import the routes
