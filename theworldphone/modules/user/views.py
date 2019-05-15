# -*- coding: utf-8 -*-
"""
    theworldphone.user.views
    ~~~~~~~~~~~~~~~~

    user views and controllers
"""

import json
from uuid import uuid4

from flask import (Blueprint, render_template, request, abort, flash, jsonify, url_for, redirect,
    Response)
from flask.ext.login import login_required, current_user
from flask.ext.babel import lazy_gettext as _

from theworldphone.extensions import db

from .constants import LANGUAGES, TEFL_PENDING, COUNTRY_CODES
from .models import User
from .forms import ProfileForm, PasswordForm


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
@user.route('/<int:offset>')
@login_required
def index(offset=0):
    """
    Creates a uuid4().hex room_id and returns

    render_template('user/index.html', user=current_user, languages=LANGUAGES, room_id=room_id)
    """
    room_id = uuid4().hex
    if current_user.is_authenticated and current_user.is_admin():
        return redirect(url_for('admin.index'))
    else:
        return render_template('user/index.html',
            user=current_user,
            languages=LANGUAGES,
            room_id=room_id)


@user.route('/details')
@login_required
def details(_id=None):
    """
    Returns details of a given user as a dictionary

    .. code-block:: javascript

        {
        'id': int,
        'name': str,
        'location': str,
        'gender': str,
        'overall': float,
        'tefl': bool
        }
    """
    if request.args.get('id'):
        user = User.get_by_id(request.args.get('id'))
        return jsonify(user.to_dict())
    abort(404)


@user.route('/request_tefl/<int:rtype>', methods=['POST'])
@login_required
def request_tefl(rtype):
    data = json.loads(request.data)

    if rtype == 0:
        user = User.get_by_id(int(data['id']))
        setattr(user, 'role_code', TEFL_PENDING)
        db.session.add(user)
        db.session.commit()

        flash("We'll be contacting you soon!", 'success')
    return jsonify({"status": "success"})


@user.route('/rate', methods=['POST'])
@login_required
def rate():
    data = json.loads(request.data)
    user = User.get_by_id(int(data['_id']))
    if user:
        _data = data['_data']
        user.set_ratings(_data)
        db.session.commit()
        return jsonify({'success': 'user vote recorded'})
    return Response(status=500, mimetype='application/json')


@user.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Return the user/profile view.
    Provides a form which allows the user to change their own

        - email
        - gender_code
        - source_langs
        - target_langs

    Validates form data & commits it to db.

    returns render_template('user/profile.html')
    """
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = ProfileForm(
        obj=user,
        email=current_user.email,
        role_code=current_user.role_code,
        status_code=current_user.status_code,
        next=request.args.get('next'))

    if form.validate_on_submit():
        form.create_profile(request, user)
        flash('Profile updated.', 'success')

    return render_template('user/profile.html',
        user=user,
        active="profile",
        form=form,
        countries=COUNTRY_CODES)


@user.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    """
        Return the user/profile view.
        Provides a form which allows the user to change their own password
    """
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = PasswordForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.update_password(user)

        flash(_('Password updated.'), 'success')

    return render_template('user/password.html',
        user=user,
        active="password",
        form=form)
