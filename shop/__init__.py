from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from shop.admin import routes


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-shop.db"
db = SQLAlchemy(app)
