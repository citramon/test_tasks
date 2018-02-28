# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField
from .models import User
from werkzeug.utils import secure_filename

class RegisterForm(Form):
    """Register form."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False
        return True


class AddFileForm(Form):
    """Add file"""
    file = FileField()

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(AddFileForm, self).__init__(*args, **kwargs)
        self.tmp = None
        self.filename = None

    def validate(self, files):
        """Validate the form."""
        initial_validation = super(AddFileForm, self).validate()
        if not initial_validation:
            return False

        if 'file' not in files:
            self.file.errors.append('No file part')
            return False

        FILE = files['file']

        if FILE.filename == '':
            self.file.errors.append('No selected file')
            return False

        self.filename = secure_filename(FILE.filename)
        self.tmp = FILE.stream.read()

        return True