from flask import render_template, url_for, flash, redirect, request, abort
from myblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from myblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from myblog.models import User, Post
import hashlib
import os
from PIL import Image
import secrets
import string

peppers = list(string.ascii_lowercase) + list(string.ascii_uppercase)


@app.route('/')
@app.route('/home')
def home():
  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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


def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _, file_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + file_ext
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
  output_size = (125, 125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)

  i.save(picture_path)
  return picture_fn


@app.route("/account", methods=['GET', 'POST'])
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
    return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash('Your post has been created!', 'success')
    return redirect(url_for('home'))
  return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)    # ! http response for forbidden route
  form = PostForm()
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit()
    flash ('Post has been updated!', 'success')
    return redirect(url_for('post', post_id=post.id))
  elif request.method == 'GET':
    form.title.data = post.title
    form.content.data = post.content
  return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403)    # ! http response for forbidden route
  db.session.delete(post)
  db.session.commit()
  flash('Your post has been deleted!', 'successs')
  return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(username=username).first_or_404()
  posts = Post.query.filter_by(author=user).\
        order_by(Post.date_posted.desc()).\
        paginate(page=page, per_page=5)
  return render_template('user_posts.html', posts=posts, user=user)