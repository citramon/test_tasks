# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for, current_app
from asdtechnology.user.models import User
from .factories import UserFactory


class TestPersonalArea:
    """Test personal area"""

    def login(self, user, testapp):
        self.user = user
        self.testapp = testapp
        self.res = self.testapp.get('/')
        form = self.res.forms['loginForm']
        form['username'] = self.user.username
        form['password'] = 'myprecious'
        self.res = form.submit().follow()

        assert self.res.status_code == 200
        assert 'You are logged in.' in self.res

    def __add_file(self, filename, contents, check='was added'):
        response = self.testapp.post(url_for('user.members'),
                                     content_type='multipart/form-data',
                                     upload_files=[('file', filename, contents)])

        self.res = response
        assert check in response
        return True

    def __rem_file(self,id):
        response = self.testapp.get(url_for('user.remove', id=id)).follow()
        self.res = response
        assert 'was remove' in response

    def test_upload_remove_file(self, user, testapp):
        """Add and remove file"""

        self.login(user, testapp)
        self.__add_file('a.bin', 'Hello')
        self.__rem_file(1)

    def test_add_over_max_files_files(self,user, testapp):
        """Try add 101 file => error"""

        self.login(user, testapp)

        for i in range(current_app.config['MAX_FILES']):
            self.__add_file('{0}.bin'.format(i), 'Hello, {0}'.format(i))

        self.__add_file('aaaa.bin', 'Hello, aaaa', 'files maximum')

        for i in range(current_app.config['MAX_FILES']):
            self.__rem_file(i+1)

    def test_add_same_files_with_different_names(self, user, testapp):
        """Add the same files with different names"""

        self.login(user, testapp)
        self.__add_file('a.bin', 'Hello')
        self.__add_file('b.bin', 'Hello', 'was found')

        self.__rem_file(1)
        self.__rem_file(2)


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert 'Invalid password' in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'myprecious'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown user' in res


class TestRegistering:
    """Register a user."""

    def test_can_register(self, user, testapp):
        """Register a new user."""
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get('/')
        # Clicks Create Account button
        res = res.click('Create account')
        # Fills out the form
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = testapp.get(url_for('public.register'))
        # Fills out form, but passwords don't match
        form = res.forms['registerForm']
        form['username'] = 'foobar'
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert 'Passwords must match' in res

    def test_sees_error_message_if_user_already_registered(self, user, testapp):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for('public.register'))
        # Fills out form, but username is already registered
        form = res.forms['registerForm']
        form['username'] = user.username
        form['email'] = 'foo@bar.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert 'Username already registered' in res
