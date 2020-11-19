from datetime import datetime
from myblog import db , login_manager
from flask_login import UserMixin




# ! letting extension grab user by id
@login_manager.user_loader
def load_user(user_id):
  return User_1.query.get(int(user_id))

class User_1(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  password = db.Column(db.String(60), nullable=False)
  posts = db.relationship('Post_1', backref='author', lazy=True)

  def __repr__(self):
    return f"User_1('{self.username}', '{self.email}', '{self.image_file}')"


class Post_1(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user_1.id'), nullable=False)

  def __repr__(self):
    return f"Post_1('{self.title}', '{self.date_posted}')"