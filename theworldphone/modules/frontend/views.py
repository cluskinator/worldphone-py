# -*- coding: utf-8 -*-
"""
    theworldphone.frontend.views
    ~~~~~~~~~~~~~~~~

    frontend views and controllers
"""

import os

from flask import (Blueprint, current_app, send_from_directory, make_response)
# from flask.ext.login import (login_required, login_user, current_user, logout_user, confirm_login,
#     login_fresh)

# from theworldphone.extensions import db, login_manager
# from theworldphone.modules.user import User, COUNTRY_CODES, LANGUAGES, ACTIVE, BANNED
# from .forms import (SignupForm, LoginForm, RecoverPasswordForm, ReauthForm, ChangePasswordForm,
#     VerifyEmailForm)


frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    return make_response(open(os.path.join(
        current_app.config['CLIENT_FOLDER'], 'src/index.html')).read())


@frontend.route('/<path:filename>')
def file(filename):
    return send_from_directory(os.path.join(
        current_app.config['CLIENT_FOLDER'], 'src/'), filename)


# @frontend.route('/signup', methods=['GET', 'POST'])
# def signup():
#     '''This function allows users to sign up for theworldphone.

#     **GET Variables:**
#         - countries : Dictionary containing country names and corresponding country codes

#     **Returns:**
#         - Index page for user if already authenticated
#         - Renders signup form with country codes if user not authenticated
#         - Sends confirmation email and redirects to signup view if user signs up successfully

#     '''
#     if current_user.is_authenticated:
#         return redirect(url_for('user.index'))

#     form = SignupForm()

#     if form.validate_on_submit():
#         user = form.signup()

#         if User.get_by_id(user.id):
#             user.activation_key = uuid.uuid4().hex
#             db.session.commit()
#             url = url_for('frontend.verify_email',
#                 email=user.email,
#                 activation_key=user.activation_key,
#                 _external=True)

#         if user.email:
#             sg = sendgrid.SendGridClient(
#                 current_app.config['SENDGRID_USERNAME'],
#                 current_app.config['SENDGRID_PASSWORD'])

#             message = sendgrid.Mail()
#             message.add_to(user.email)
#             message.set_subject('The World Phone -- Please Verify your Email')
#             message.set_from('The World Phone <no-reply@theworldphone.com>')
#             message.set_html(
#                 render_template('emails/_verify.html',
#                     project=current_app.config['PROJECT'],
#                     username=user.name,
#                     url=url))
#             status, msg = sg.send(message)

#         flash(_('Please check your email for a link to register.'), 'success')
#         return redirect(url_for('frontend.signup'))

#     countries = json.dumps(COUNTRY_CODES).encode('utf-8')
#     return render_template('frontend/signup.html', form=form, countries=countries)


# @frontend.route('/')
# def index():
#     '''This function redirects the user to the proper index page
#     based on their credentials.


#     Returns:
#         Template for an admin user's index page, template for a logged in
#         user's index page, or the home page for the worldphone for an
#         unauthenticated user.

#     '''
#     if current_user.is_authenticated and current_user.is_admin():
#         return redirect(url_for('admin.index'))
#     elif current_user.is_authenticated:
#         return redirect(url_for('user.index'))
#     return render_template('index.html', page_title="The World Phone")


# @frontend.route('/login', methods=['GET', 'POST'])
# def login():
#     '''
#     If user is not logged in:

#     1) Show the user the login form.
#     2) Handle the input form the login form.

#     If user is already logged, send them to user.index or admin.index as appropriate

#     If User.authenticate(form.login.data, form.password.data) checks out
#     send them to user.index or admin.index as appropriate.

#     If the user is banned, flash a message and reshow login form.

#     '''
#     if current_user.is_authenticated and not current_user.is_admin():
#         return redirect(url_for('user.index'))
#     elif current_user.is_authenticated and current_user.is_admin():
#         return redirect(url_for('admin.index'))

#     form = LoginForm(login=request.args.get('login', None),
#                      next=request.args.get('next', None))

#     if form.validate_on_submit():
#         user, authenticated = User.authenticate(form.login.data,
#                                     form.password.data)
#         if user and authenticated and user.status_code == BANNED:
#             flash(_('Sorry, you are not allowed access to your account due to inappropriate behavior.'), 'danger')
#         elif user and authenticated and user.status_code == ACTIVE:
#             remember = request.form.get('remember') == 'y'
#             if login_user(user, remember=remember):

#                 if request.environ.get('HTTP_X_REAL_IP', request.remote_addr) not in user._ip_list.values():
#                     user._ip_list[datetime.datetime.now()] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
#                     db.session.commit()

#                 flash(_("Logged in"), 'success')
#             if user.is_admin():
#                 return redirect(url_for('admin.index'))
#             else:
#                 return redirect(form.next.data or url_for('user.index'))
#         else:
#             flash(_('Sorry, invalid login'), 'danger')

#     return render_template('frontend/login.html', form=form)


# @frontend.route('/reauth', methods=['GET', 'POST'])
# @login_required
# def reauth():
#     '''This function allows a user to attempt to log in
#     again after a failed attempt.

#     **Returns:**
#         - Change password view on reauthentication success
#         - Reauthentication view on reauthentication failure.

#     '''
#     form = ReauthForm(next=request.args.get('next'))

#     if request.method == 'POST':
#         user, authenticated = User.authenticate(current_user.name,
#                                     form.password.data)
#         if user and authenticated:
#             confirm_login()
#             current_app.logger.debug('reauth: %s' % session['_fresh'])
#             flash(_('Reauthenticated.'), 'success')
#             return redirect('/change_password')

#         flash(_('Password is wrong.'), 'danger')
#     return render_template('frontend/reauth.html', form=form)


# @frontend.route('/logout')
# @login_required
# def logout():
#     '''This function logs user out of current session.

#     Returns:
#         Redirects to login view on success.

#     '''
#     logout_user()
#     flash(_('Logged out'), 'success')
#     return redirect(url_for('frontend.login'))


# @frontend.route('/verify_email', methods=['GET', 'POST'])
# def verify_email():
#     '''This function verifies a user after the user receives the validation email.

#     **POST Variables:**
#         - activation_key: A user's unique activation key needed for authentication
#         - email: The email address the user clicked the activation link from.

#     **Returns:**
#         - Refreshes login manager if need be
#         - 403 if user does not exist in database, or is banned
#         - Renders "frontend/verify_email.html" template on success
#         - Redirects to login view after user submits and validates info

#     '''
#     user = None
#     if current_user.is_authenticated:
#         if not login_fresh():
#             return login_manager.needs_refresh()
#         user = current_user
#     elif 'activation_key' in request.values and 'email' in request.values:
#         activation_key = request.values['activation_key']
#         email = request.values['email']
#         user = User.query.filter_by(activation_key=activation_key).filter_by(email=email).first()

#     if user is None or user.status_code == BANNED:
#         abort(403)

#     form = VerifyEmailForm(obj=user)

#     if form.validate_on_submit():
#         form.verify(user)
#         flash(_("You've been verified! You can now login."), "success")
#         return redirect(url_for("frontend.login"))

#     return render_template("frontend/verify_email.html", user=user, form=form, languages=LANGUAGES)


# @frontend.route('/change_password', methods=['GET', 'POST'])
# def change_password():
#     '''This function provides a mechanism by which the user can change their password.

#     **POST Variables:**
#         - activation_key: The user's unique activation key
#         - email: The email address the user received the activation email in

#     **Returns:**
#         - Refreshes login manager if need be
#         - 403 if user does not exist in database or is banned
#         - Renders "frontend/change_password.html" template on success
#         - Redirects to login view if password change submission is successful

#     '''
#     user = None
#     if current_user.is_authenticated:
#         if not login_fresh():
#             return login_manager.needs_refresh()
#         user = current_user
#     elif 'activation_key' in request.values and 'email' in request.values:
#         activation_key = request.values['activation_key']
#         email = request.values['email']
#         user = User.query.filter_by(activation_key=activation_key).filter_by(email=email).first()

#     if user is None or user.status_code != ACTIVE:
#         abort(403)

#     form = ChangePasswordForm(activation_key=user.activation_key)

#     if form.validate_on_submit():
#         user.change_password()

#         flash(_("Your password has been changed, please log in again"),
#               "success")
#         return redirect(url_for("frontend.login"))

#     return render_template("frontend/change_password.html", form=form)


# @frontend.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     '''This function sends the user an email that instructs them on how to reset their password.

#     **POST Variables:**
#         - email: The user's email address

#     **Returns:**
#         - Renders "frontend/reset_password.html" template on success
#     '''
#     form = RecoverPasswordForm()

#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()

#         if user and user.status_code == ACTIVE:
#             if user.email:
#                 url = url_for(
#                     'frontend.change_password',
#                     email=user.email,
#                     activation_key=user.activation_key,
#                     _external=True)
#                 sg = sendgrid.SendGridClient(
#                     current_app.config['SENDGRID_USERNAME'],
#                     current_app.config['SENDGRID_PASSWORD'])

#                 message = sendgrid.Mail()
#                 message.add_to(user.email)
#                 message.set_subject('The World Phone -- Reset your password')
#                 message.set_from('The World Phone <bots@theworldphone.com>')
#                 message.set_html(
#                     render_template('macros/_reset_password.html',
#                     project=current_app.config['PROJECT'],
#                     username=user.name,
#                     url=url))
#                 status, msg = sg.send(message)

#             user.reset_password()
#             flash('Please see your email for instructions on how to access your account', 'success')
#             return render_template('frontend/reset_password.html', form=form)
#         else:
#             flash(_('Sorry, no user found with that email address. Did you verify your email?'), 'danger')

#     return render_template('frontend/reset_password.html', form=form)
