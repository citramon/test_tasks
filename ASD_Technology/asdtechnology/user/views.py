# -*- coding: utf-8 -*-
"""User views."""
import os
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from asdtechnology.user.forms import AddFileForm
blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')
from asdtechnology.utils import flash_errors

from asdtechnology.user.models import User, File, Ufile
import hashlib
from Crypto.Hash import SHA256

@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def members():
    """List files."""
    form = AddFileForm(request.form)
    if form.is_submitted() and form.validate(request.files):
        # Add file

        count = Ufile.query.filter_by(user_id=current_user.id).count()
        if count >= current_app.config['MAX_FILES']:
            flash('{0} files maximum!'.format(current_app.config['MAX_FILES']), 'info')

        else:

            filemd5 = hashlib.md5(form.tmp).hexdigest()
            link = SHA256.new(form.filename + str(datetime.now())).hexdigest()
            res = File.query.filter_by(filemd5=filemd5).first()

            if res:
                another_file = Ufile.query.filter_by(file_id=res.id).first()
                another_user = User.query.filter_by(id=another_file.user_id).first()

                Ufile.create(filename=form.filename, file_id=res.id, user_id=current_user.id, link=link)

                flash('The file was found by the user: {0} with name: {1}'.format(
                    another_user.username, another_file.filename
                ), 'success')

            else:
                with open(os.path.join(current_app.config['FILE_DIR'], link), "w") as f:
                    f.write(form.tmp)
                    File.create(filename=f.name.replace('{0}/'.format(current_app.config['FILE_DIR']), ''),
                                filepath=current_app.config['FILE_DIR'], filemd5=filemd5)
                    new = File.query.filter_by(filemd5=filemd5).first()
                    Ufile.create(filename=form.filename, file_id=new.id, user_id=current_user.id, link=link)

                    flash('The file {0} was added'.format(form.filename), 'success')

    else:
        flash_errors(form)

    page = request.args.get('page', 1, type=int)
    pagination = Ufile.query.filter_by(user_id=current_user.id).paginate(
        page, per_page=current_app.config['FILES_PER_PAGE'], error_out=False
    )
    ufiles = pagination.items

    return render_template('users/members.html',
                           form=form,
                           ufiles=ufiles,
                           pagination=pagination,
                           max_files=current_app.config['MAX_FILES'])


@blueprint.route('/remove/<int:id>')
@login_required
def remove(id):
    ufile = Ufile.query.filter_by(id=id).first()

    if not ufile:
        flash('File with id {0} not found'.format(id), 'info')
    else:
        file_id = ufile.file_id
        ufile.delete()

        file = File.query.filter_by(id=file_id).first()
        if len(file.ufiles) == 0:
            os.remove(os.path.join(file.filepath, file.filename))
            file.delete()


        flash('File {0} was remove'.format(ufile.filename), 'success')

    return redirect('users/')


