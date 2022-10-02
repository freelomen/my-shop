from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from shop.admin import routes


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my-shop.db"
app.config['SECRET_KEY'] = 'xdrfghjk2345klkjmhgcv'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
