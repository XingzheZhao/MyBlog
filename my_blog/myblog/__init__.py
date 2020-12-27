from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from myblog.config import Config
import os

load_dotenv()


con = f'mysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DB")}'

db = SQLAlchemy()
# bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'    # for login required page
login_manager.login_message_category = 'info'   # ! login messagecolor blue
mail = Mail()


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)

  from myblog.users.routes import users
  from myblog.posts.routes import posts
  from myblog.main.routes import main
  from myblog.errors.handlers import errors

  app.register_blueprint(users)
  app.register_blueprint(posts)
  app.register_blueprint(main)
  app.register_blueprint(errors)
  

  return app
