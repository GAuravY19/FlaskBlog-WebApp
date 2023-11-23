from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegisterationForm, LoginForm, ProfileUpdate, NewPosts
from flaskblog.models import User, Post
from flask_login import login_user, login_required, logout_user, current_user
from flaskblog import app, bcrypt, db
import os
import secrets
from PIL import Image

# Home Route
@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    return render_template('home.html', posts = posts)


# About Page Route
@app.route('/about')
def about():
    return render_template('about.html')


# Contact Page Route
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Sign Up Page Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegisterationForm()
    if form.validate_on_submit():

        hashed_pw = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')

        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)

        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}!", 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form = form)


# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email = form.email.data).first()

            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_link = request.args.get('next')

                flash('Login Successful!', 'success')
                return redirect(url_for('account')) if next_link else redirect(url_for('home'))

            else:
                flash('Login Unsuccessful! Please check email and password.','danger')

    return render_template('login.html', form = form)


# Logout Page Route
@app.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('home'))


# Function For saving User's Profile Photo
def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_picture.filename)

    picture_name = random_hex + f_ext
    picture_path = os.path.join(app.root_path+ '/static/profile_pics/'+ picture_name)

    output_size = (125, 125)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_name


# Account Page Route
@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = ProfileUpdate()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_url = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash('Account Updated successfully!', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':

        form.username.data = current_user.username
        form.email.data = current_user.email

    image_url = url_for('static', filename= 'profile_pics/'+ current_user.image_url)

    return render_template('account.html', form=form, image_url = image_url)


# Creating Post Page Route
@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_posts():
    form = NewPosts()

    if form.validate_on_submit():

        posts = Post(title = form.title.data,
                     content = form.content.data,
                     author = current_user)

        db.session.add(posts)
        db.session.commit()

        flash('Post created successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('new_post.html', form=form)


# Viewing a Post Route
@app.route('/post/<int:post_id>')
def posts(post_id):
    posts = Post.query.get_or_404(post_id)

    return render_template('post.html', posts = posts)


# Updating a existing post route
@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    form = NewPosts()
    posts = Post.query.get_or_404(post_id)

    if posts.author != current_user:
        abort(403)

    if form.validate_on_submit():
        posts.title = form.title.data
        posts.content = form.content.data

        db.session.commit()

        flash('Post updated successfully!', 'success')
        return redirect(url_for('posts', post_id = post_id))

    elif request.method == 'GET':
        form.title.data = posts.title
        form.content.data = posts.content

    return render_template('update_post.html', form = form)


# Deleting a post Route
@app.route('/post/<int:post_id>/delete', methods = ['GET', 'POST'])
@login_required
def delete_post(post_id):
    posts = Post.query.get_or_404(post_id)

    if posts.author != current_user:
        abort(403)

    db.session.delete(posts)
    db.session.commit()

    return redirect(url_for('home'))


# Route for viewing any particular user's posts
@app.route('/posts/<string:username>')
def user_posts(username):
    user = User.query.filter_by(username = username).first_or_404()
    page = request.args.get('page', default=1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts = posts, user = user)

