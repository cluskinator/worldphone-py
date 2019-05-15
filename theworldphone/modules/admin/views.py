# -*- coding: utf-8 -*-
"""
    theworldphone.modules.admin.views
    ~~~~~~~~~~~~~~~~

    admin module views and controllers
"""

from werkzeug import secure_filename
import os, json, urllib, re, requests, time, datetime

from itertools import chain

from flask import (Blueprint, render_template, request, flash, current_app, send_from_directory,
    redirect, url_for, jsonify, abort)
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.babel import Babel

from theworldphone.extensions import db
from theworldphone.decorators import admin_required

from theworldphone.modules.frontend.forms import LoginForm
from theworldphone.modules.redis import RedisQueue
from theworldphone.modules.user.models import User, Language
from theworldphone.modules.user.constants import UserRole, COUNTRY_CODES
from theworldphone.modules.call import CallLog
from theworldphone.modules.call.constants import CallType

from .forms import UserForm, EditTranslationForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


# flash(_( -> flash((

@admin.route('/login', methods=['GET', 'POST'])
def login():
    '''
    If user is not logged in:

    1) Show the user the login form.
    2) Handle the input form the login form.

    If user is already logged, send them to user.index or admin.index as appropriate

    If User.authenticate(form.login.data, form.password.data) checks out
    send them to user.index or admin.index as appropriate.

    If the user is banned, flash a message and reshow login form.

    '''
    if current_user.is_authenticated and not current_user.is_admin():
        return redirect(url_for('user.index'))
    elif current_user.is_authenticated and current_user.is_admin():
        return redirect(url_for('admin.index'))

    form = LoginForm(login=request.args.get('login', None),
                     next=request.args.get('next', None))

    if form.validate_on_submit():
        user, authenticated = User.authenticate(form.login.data,
                                    form.password.data)
        if user and authenticated and user.status == 'banned':
            flash(('Sorry, you are not allowed access to your account due to inappropriate behavior.'), 'danger')
        elif user and authenticated and user.status == 'active':
            remember = request.form.get('remember') == 'y'
            if login_user(user, remember=remember):

                if request.environ.get('HTTP_X_REAL_IP', request.remote_addr) not in user._ip_list.values():
                    user._ip_list[datetime.datetime.now()] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                    db.session.commit()

                flash(("Logged in"), 'success')
            if user.is_admin():
                return redirect(url_for('admin.index'))
            else:
                return redirect(form.next.data or url_for('user.index'))
        else:
            flash(('Sorry, invalid login'), 'danger')

    return render_template('frontend/login.html', form=form)


@admin.route('/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
    '''This function allows a user to attempt to log in
    again after a failed attempt.

    **Returns:**
        - Change password view on reauthentication success
        - Reauthentication view on reauthentication failure.

    '''
    form = ReauthForm(next=request.args.get('next'))

    if request.method == 'POST':
        user, authenticated = User.authenticate(current_user.name,
                                    form.password.data)
        if user and authenticated:
            confirm_login()
            current_app.logger.debug('reauth: %s' % session['_fresh'])
            flash(('Reauthenticated.'), 'success')
            return redirect('/change_password')

        flash(('Password is wrong.'), 'danger')
    return render_template('frontend/reauth.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    '''This function logs user out of current session.

    Returns:
        Redirects to login view on success.

    '''
    logout_user()
    flash(('Logged out'), 'success')
    return redirect(url_for('admin.login'))


@admin.route('/')
@login_required
@admin_required
def index():
    """
    # Grab TEFL_PENDING users and flagged calls.
    Grab all users.
    Use those to load admin index page.

    # Returns render_template('admin/index.html', users=users, active='users', calls=calls)
    Returns render_template('admin/users.html', users=users, active='users', title='Users', countries=COUNTRY_CODES)
    """
    # users = User.query.filter_by(_role_code=UserRole.tefl_pending.value)
    # calls = CallLog.query.filter_by(flagged=True)
    # return render_template('admin/index.html',
    #     users=users,
    #     active='users',
    #     calls=calls)
    users = User.query.all()
    return render_template('admin/users.html',
        users=users,
        active='users',
        title='Users',
        countries=COUNTRY_CODES)


@admin.route('/users')
@login_required
@admin_required
def users():
    """
    Get all users and user those to load admin/users/.
    The users view contains a table filled with details about all users in the system.

    Returns render_template('admin/users.html', users=users, active='users')

    """
    users = User.query.all()
    return render_template('admin/users.html',
        users=users,
        active='users',
        title='Users',
        countries=COUNTRY_CODES)


@admin.route('/user/<string:user_uid>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_uid):
    """
    Allows the admin to change the following details about the user:

    - _role_code
    - status (_status_code)
    - created_time

    If the user does not exist, returns a 404.

    Returns render_template('admin/user.html')

    """
    user = User.query.filter_by(uid=user_uid).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.save(user)
        flash('User updated.', 'success')

    return render_template('admin/user.html',
        user=user,
        form=form,
        countries=COUNTRY_CODES)


@admin.route('/ban_user', methods=['POST'])
@login_required
@admin_required
def ban_user():
    """
    Bans a user
    """
    data = json.loads(request.data)
    uids = data['uids']

    if isinstance(uids, list):
        for user_uid in uids:
            ban(user_uid)
        time.sleep(0.75)
        return jsonify(flag='success', message='all users banned.')
    else:
        user_uid = uids
        ban(user_uid)
        time.sleep(0.75)
        return jsonify(flag='success', message='User ' + user_uid + ' was banned.')
    return jsonify(flag='error', message='invalid operation')


@admin.route('/tefl_users')
@login_required
@admin_required
def tefl_users():
    """
    Displays information about all TEFL users.
    Uses the same html as /users/ view
    """
    users = User.query.filter_by(_role_code=UserRole.tefl.value)
    return render_template('admin/users.html',
        users=users,
        active='users',
        title='TEFL Users',
        countries=COUNTRY_CODES)


@admin.route('/pending_tefl_users')
@login_required
@admin_required
def pending_tefl_users():
    """
    Displays information about all pending TEFL users.
    Uses the same html as /users/ view
    """

    users = User.query.filter_by(_role_code=UserRole.tefl_pending.value)
    return render_template('admin/pending_tefl_users.html', users=users, active='users')


@admin.route('/appr_tefl/<string:uid>/<int:code>')
@login_required
@admin_required
def appr_tefl(uid, code):
    """
    Args:
        id (int): id of user
        code (int): 0 is deny, 1 is approve

    Changes User._role_code for a given user in the db.
    """
    user = User().first(uid=uid)
    if code is 0:
        user.role = 'tefl_denied'
        db.session.add(user)
        db.session.commit()
    elif code is 1:
        user.role = 'tefl'
        db.session.add(user)
        db.session.commit()

    users = User.query.filter_by(_role_code=UserRole.tefl_pending.value)
    return render_template('admin/pending_tefl_users.html', users=users, active='users')


@admin.route('/translation/edit/<language>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_translation(language):
    """
    """
    form = EditTranslationForm(language=language)
    if form.validate_on_submit():
        file = request.files[form.file.name]
        if file:
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(current_app.config['TRANSLATIONS_FOLDER'], language,
                    current_app.config['TRANSLATIONS_PATH'],
                    current_app.config['TRANSALTIONS_FILE']))
            os.system("pybabel compile -f -d theworldphone/translations")
            flash("Translation File has been uploaded")
            return redirect(url_for('admin.edit_translation', language=language))
    return render_template('admin/translation.html', form=form)


@admin.route('/translations', methods=['GET'])
@login_required
@admin_required
def translations():
    babel = Babel(current_app)
    languages = babel.list_translations()
    return render_template('admin/translations.html', languages=languages)


@admin.route('/translation/<language>', methods=['GET'])
@login_required
@admin_required
def existing_translation(language):
    return send_from_directory(os.path.join(
        current_app.config['TRANSLATIONS_FOLDER'],
        language,
        current_app.config['TRANSLATIONS_PATH']),
        current_app.config['TRANSALTIONS_FILE'])


@admin.route('/calls', methods=['GET'])
@login_required
@admin_required
def calls():
    """
    Get all calls and use those to load admin/calls/.
    The calls view contains a table filled with details about all calls in the system.

    return render_template('admin/calls.html', calls=calls)
    """
    calls = CallLog().all()
    return render_template('admin/calls.html', calls=calls)


@admin.route('/flagged_calls', methods=['GET'])
@login_required
@admin_required
def flagged_calls():
    """
    Get all flagged calls and use those to load admin/calls/.
    The calls view contains a table filled with details about all calls in the system.

    return render_template('admin/calls.html', calls=calls)
    """
    calls = CallLog.query.filter_by(flagged=True)
    return render_template('admin/flagged_calls.html', calls=calls)


@admin.route('/get_call_details', methods=['GET', 'POST'])
@login_required
@admin_required
def get_call_details():
    call_uid = json.loads(request.data)
    call = CallLog().first(uid=call_uid)
    caller_status = User().first(uid=call.caller_uid).status
    callee_status = User().first(uid=call.callee_uid).status
    return jsonify({
        'html': render_template('admin/partials/flagged_details.html',
            caller_status=caller_status,
            callee_status=callee_status,
            call=call)})


@admin.route('/countries', methods=['GET'])
@login_required
@admin_required
def countries():
    users = User.query.filter_by()
    role_names = [role.name for role in UserRole]
    country_counts = {}

    for user in users:
        if user.location:
            locale = COUNTRY_CODES[user.location]

            # If we haven't seen this locale yet, add it to the dict
            if locale not in country_counts.keys():
                country_counts[locale] = {}
                country_counts[locale]['total'] = 0

                # Then add each possible user role to the dict at 0
                for role in role_names:
                    country_counts[locale][role] = 0

            country_counts[locale][user.role] += 1
            country_counts[locale]['total'] += 1

    return render_template('admin/countries.html',
        country_counts=country_counts,
        role_names=role_names)


# @admin.route('/ips_to_geo', methods=['GET'])
# @login_required
# @admin_required
# def ips_to_geo():
#
#     """
#     Get the lat/long of all current calls from redis queue.
#     Returns json which looks like:
#
#     .. code-block:: javascript
#
#         {
#             count: 2,
#             points: [{
#                  'city': 'Tallahassee',
#                  'latlng': [30.4550, 84.2555],
#                 },
#                 {
#                  'city': 'Orlando',
#                  'latlng': [38.3217, 81.2245],
#                 }
#         }
#     """
#     tracking_queue = RedisQueue('current_calls', **current_app.config['REDIS_CONFIG'])
#     calls = [call.split(':') for call in tracking_queue.all()]
#
#     if request.args.get('latlng'):
#         # match all elements in the nested call lists of tracking_queue to IP pattern
#         pattern = re.compile(".*\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
#         ip_list = list(chain.from_iterable([[i for i in call if pattern.match(i)] for call in calls]))
#
#         # geoencode those IP addresses and drop that JSON to the caller
#         geo_list = []
#         for ip in ip_list:
#             # Works, at least when freegeoip.net isn't returning intermittent 503s
#             url = 'http://freegeoip.net/json/%s' % ip
#
#             try:
#                 response = requests.get(url)
#                 if response:
#                     j = response.json()
#                     lat = j.get('latitude')
#                     lng = j.get('longitude')
#                     if lat and lng:
#                         geo_list.append({'latlng': [lat, lng]})
#
#             except requests.ConnectionError as err:
#                 print(err)
#
#         points_list = [x['latlng'] for x in geo_list]
#         return jsonify({'count': len(points_list), 'points': points_list})
#     # if all else(s) fail(s), bail
#     abort(404)


# def get_geo_ip(s, _dict={}, _list=[]):
#     for line in s.split('\n'):
#         if line.startswith('City:'):
#             _dict['city'] = line[6:]
#         elif line.startswith('Latitude:'):
#             if line[10:]:
#                 _list.append(float(line[10:]))
#         elif line.startswith('Longitude:'):
#             if line[11:]:
#                 _list.append(float(line[11:]))
#     if _list:
#         _dict['latlng'] = _list
#         return _dict
#     return False


def ban(user_uid):
    user = User().first(uid=user_uid)
    if user and not user.status == 'banned':
        user.status = 'banned'
        db.session.commit()
