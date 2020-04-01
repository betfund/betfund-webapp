from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from application import login_manager
from application.forms import LogInForm
from application.models import User

login_bp = Blueprint('login_bp', __name__, template_folder='templates')


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    End point for login page.

    GET:    Redirects user to their dashboard if they are logged in.
    POST:   Attempts a login; if fail, reaches redirect back with error messages.
    """

    # redirect user to dashboard if they are authenticated
    if current_user.is_authenticated:
        return redirect(url_for('loggedin_bp.dashboard'))

    login_form = LogInForm()
    if request.method == 'POST':

        # check to make sure the form is valid
        if login_form.validate_on_submit():

            # get the email address and password
            email_address = login_form.email_address.data
            password = login_form.password.data

            # get the user info
            user = User.query.filter_by(email_address=email_address).first()

            # if the password is correct, the log the user in and
            # redirect them to the dashboard
            if user and user.check_password(password=password):
                login_user(user)
                return redirect(url_for('loggedin_bp.dashboard'))

        # otherwise, tell them the password is invalid
        # and send them back to the login page to try again
        flash('Invalid email/password combination')
        return redirect(url_for('login_bp.login'))

    # notify of any form errors
    for error_type, error_messages in login_form.errors.items():
        for message in error_messages:
            flash(message)

    return render_template(
        'login_form.html',
        form=login_form,
        title='Log in',
    )


@login_bp.route("/logout")
@login_required
def logout():
    """
    End point for log out.

    GET: Logs out a user and redirects them to login page.
    """
    logout_user()
    return redirect(url_for('login_bp.login'))


@login_manager.user_loader
def load_user(user_id):
    """
    Check if user is logged-in on every page load.
    """
    if user_id is not None:
        return User.query.get(user_id)
    return None
