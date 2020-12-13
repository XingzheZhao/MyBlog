from flask import render_template, url_for, flash, redirect, request
from myblog.forms import RegistrationForm, LoginForm
from myblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from myblog.models import User, Post
import hashlib
import secrets
import string

peppers = list(string.ascii_lowercase) + list(string.ascii_uppercase)

posts = [
  {
    'author': 'SamZ',
    'title': 'Blog Post 1',
    'content': 'First post content',
    'date_posted': 'April 20, 2020'
  },
  {
    'author': 'Peter Parker',
    'title': 'Blog Post 2',
    'content': 'Second post content',
    'date_posted': 'December 20, 2020'
  }
]

@app.route('/')
@app.route('/home')
def home():
  return render_template('home.html', posts=posts)


@app.route("/about")
def about():
  return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    # hashed_password = make_pw_hash(form.password.data)
    pw_salt = secrets.token_urlsafe(10)
    hashed_password = hashlib.pbkdf2_hmac('sha256', str.encode(form.password.data), str.encode(pw_salt+secrets.choice(peppers)), 10000).hex()
    user = User(username=form.username.data, email=form.email.data, password=hashed_password, salt=pw_salt)
    db.session.add(user)
    db.session.commit()
    flash('Your accoutn has been created! You are now able to log in', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  isValidPW = False  # flag to check if password mataches
  if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      # if user and bcrypt.check_password_hash(user.password, form.password.data):
      # if user and check_pw_hash:
      if user:
        for pepper in peppers:
          if hashlib.pbkdf2_hmac('sha256', str.encode(form.password.data), str.encode(user.salt+pepper), 10000).hex() == user.password:
            isValidPW = True
            break

        if isValidPW:
          login_user(user, remember=form.remember.data)
          next_page = request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for('account'))
        else:
          flash('Login Unsuccessfully. Please check email and password', 'danger')
      else:
        flash('Login Unsuccessfully, User does not exist!')
  return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
  return render_template('account.html', title='Account')