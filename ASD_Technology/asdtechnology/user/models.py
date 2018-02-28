# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin

from asdtechnology.database import Column, Model, SurrogatePK, db, reference_col, relationship
from asdtechnology.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    user_id = reference_col('users', nullable=True)
    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    files = db.relationship('Ufile', backref='file')

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)


class File(SurrogatePK, Model):
    """A file of the app."""

    __tablename__ = 'files'
    filename = Column(db.String(80), unique=True, nullable=False)
    filepath = Column(db.String(80), nullable=False)
    filemd5 = Column(db.String(80), unique=True, nullable=False)
    ufiles = db.relationship('Ufile', backref='ufiles')

    def __init__(self, filename, filepath, filemd5, **kwargs):
        """Create instance."""
        db.Model.__init__(self, filename=filename, filepath=filepath, filemd5=filemd5, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<File({name})>'.format(name=self.filename)


class Ufile(SurrogatePK, Model):
    """A userfile of the app."""

    __tablename__ = 'ufiles'
    filename = Column(db.String(80), nullable=False)
    file_id = Column(db.Integer, db.ForeignKey('files.id'))
    user_id = Column(db.Integer, db.ForeignKey('users.id'))
    link = Column(db.String(80), nullable=False)

    def __init__(self, filename, file_id, user_id, **kwargs):
        """Create instance."""
        db.Model.__init__(self, filename=filename, file_id=file_id, user_id=user_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Ufile({name})>'.format(name=self.filename)