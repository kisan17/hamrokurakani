from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from hamrokurakani import bcrypt, db
from hamrokurakani.core.utils import human_date, save_picture
from hamrokurakani.models import User
from hamrokurakani.users.forms import LoginForm, RegistrationForm, UpdateAccountForm

users = Blueprint('users', __name__, template_folder='templates')


@users.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now()
        db.session.commit()


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('chat.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your  account has been created! Happy Staying!!', 'success')
        return redirect(url_for('users.login'))
    return render_template('users/register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('chat.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            db.session.commit()
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('chat.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('users/login.html', title='Login', form=form)


@users.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    date = human_date(current_user.joined)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            picture_file = save_picture(username, form.picture.data)
            current_user.image_file = picture_file
        current_user.fullname = form.fullname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.settings'))
    elif request.method == 'GET':
        form.fullname.data = current_user.fullname
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.picture.data = current_user.image_file
    image_file = url_for(
        'static', filename='profilepics/' + current_user.image_file)
    return render_template('users/setting.html', title='Account', image_file=image_file, form=form, date=date)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.login'))
