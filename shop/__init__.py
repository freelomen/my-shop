from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shop.admin import routes


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
# create the extension
db = SQLAlchemy(app)