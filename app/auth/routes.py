from flask import render_template, redirect, request, flash, url_for
from flask_babel import _
from flask_login import login_user, logout_user, current_user
from werkzeug.urls import url_parse

from app.auth import bp
from app.auth import email
from app.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, \
    ResetPasswordForm
from app.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(form.username.data)
        user_ = User.get_user_by_username(form.username.data)
        if not user_ or not user_.check_password(form.password.data):
            flash(_('Invalid Username or password'))
            return redirect(url_for('auth.login'))
        login_user(user_, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('main.index'))
        return redirect(url_for('main.index'))

    return render_template('auth/login.html', form=form, title='Sign In')


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_ = User(username=form.username.data,
                     email=form.email.data,
                     password=form.password.data)
        user_.add_user(user_)
        flash(_('Congrats you registered successfully'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='register', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user_ = User.get_user_by_email(form.email.data)
        if user_:
            email.send_password_reset_email(user_)
        flash(_('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password',
                           form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user_ = User.verify_reset_password_token(token)
    if not user_:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_.set_password(form.password.data)
        flash(_('Your Password has been reset'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
