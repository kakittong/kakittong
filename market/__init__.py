from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:26462878@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'IjkyZjMzMDAxMjIwMzM0YWFmOTM5Mjg2NmRjNTVkOGI4YjMwZjhjY2Ei.ZJ52tQ.D5d56gEfqgUBOqGQzmjocvclVbo'
# app.config['WTF_CSRF_ENABLED'] = False
app.config['DEBUG'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from market import routes
