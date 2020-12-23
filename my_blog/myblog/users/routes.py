from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from myblog import db
from myblog.models import User, Post
from myblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm)
from myblog.users.utils import save_picture, send_reset_email
import hashlib
import secrets
import string

peppers = list(string.ascii_lowercase) + list(string.ascii_uppercase)

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    pw_salt = secrets.token_urlsafe(10)
    hashed_password = hashlib.pbkdf2_hmac('sha256', str.encode(form.password.data), str.encode(pw_salt+secrets.choice(peppers)), 10000).hex()
    user = User(username=form.username.data, email=form.email.data, password=hashed_password, salt=pw_salt)
    db.session.add(user)
    db.session.commit()
    flash('Your accoutn has been created! You are now able to log in', 'success')
    return redirect(url_for('users.login'))
  return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = LoginForm()
  isValidPW = False  # flag to check if password mataches
  if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()
      # if user and bcrypt.check_password_hash(user.password, form.password.data):
      if user:
        for pepper in peppers:
          if hashlib.pbkdf2_hmac('sha256', str.encode(form.password.data), str.encode(user.salt+pepper), 10000).hex() == user.password:
            isValidPW = True
            break

        if isValidPW:
          login_user(user, remember=form.remember.data)
          next_page = request.args.get('next')
          return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
          flash('Login Unsuccessfully. Please check email and password', 'danger')
      else:
        flash('Login Unsuccessfully, User does not exist!')
  return render_template('login.html', title='Login', form=form)



@users.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('main.home'))



@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash("Your account has bee updated!", 'success')
    return redirect(url_for('users.account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  posts = Post.query.filter_by(author=user).\
        order_by(Post.date_posted.desc()).\
        paginate(page=page, per_page=5)
  return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    send_reset_email(user)
    flash('An email has been sent with instructions to reset your password', 'info')
    return redirect(url_for('users.login'))
  return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  user = User.verify_reset_token(token)
  if not user:
    flash('Sorry, The token is invalid or expired!', 'warning')
    return redirect(url_for('users.reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    # hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    pw_salt = secrets.token_urlsafe(10)
    hashed_password = hashlib.pbkdf2_hmac('sha256', str.encode(form.password.data), str.encode(pw_salt+secrets.choice(peppers)), 10000).hex()
    user.salt = pw_salt
    user.password = hashed_password
    db.session.commit()
    flash('Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('users.login'))
  return render_template('reset_token.html', title='Reset Password', form=form)