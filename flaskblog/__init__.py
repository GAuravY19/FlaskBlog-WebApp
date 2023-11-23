from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import login_required, LoginManager, login_user

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'c31f7cbeec8acf4bc418189acb0fd41e366f0bef75e4790497398a7378dd0cccd46257401fa4c225a55c2362f4a66d98c2a97ba48b05f032b23da593f8c637b0eae8abdccedf1e8d20753ce46130d4541ca99cb2e4345c8cbd1947b5f7c9402a85ffbb8452f07199d13fc225a72af4dceb3b1c4d3881fb304c47b769fe854444'
app.app_context().push()

bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'
loginmanager.login_message_category = 'danger'

db = SQLAlchemy(app)

from flaskblog import routes

