from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

load_dotenv()



app = Flask(__name__)
con = f'mysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PASSWORD")}@{os.getenv("MYSQL_HOST")}/{os.getenv("MYSQL_DB")}'

app.config['SECRET_KEY']=os.getenv("APP_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = con
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'   # ! login messagecolor blue

from myblog import routes
