from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from application import login_manager
from application.forms import SearchForm

loggedin_bp = Blueprint('loggedin_bp', __name__, template_folder='templates')


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Redirects an unaurhtorize user to login page."""
    return redirect(url_for('login_bp.login'))


@loggedin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Dashboard route.

    TODO: This will be updated.
    """
    search_form = SearchForm()

    return render_template(
        'dashboard.html',
        title='Dashboard',
        form=search_form
    )
