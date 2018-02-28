# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, send_from_directory, abort
from flask_login import login_required, login_user, logout_user

from asdtechnology.extensions import login_manager
from asdtechnology.public.forms import LoginForm
from asdtechnology.user.forms import RegisterForm
from asdtechnology.user.models import User, Ufile, File
from asdtechnology.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)

@blueprint.route('/download/<link>')
def download(link):
    """Download files."""
    check_link = Ufile.query.filter_by(link=link).first()
    if not check_link :
        abort(404)
    download_file = File.query.filter_by(id=check_link.file_id).first()
    if not download_file:
        abort(404)

    return send_from_directory(download_file.filepath,
                           download_file.filename,
                           as_attachment=True,
                           attachment_filename=check_link.filename)