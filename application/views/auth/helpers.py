from flask import flash, redirect, url_for

from application import login_manager
from application.models import User


@login_manager.user_loader
def load_user(user_id):
    """
    Check if user is logged-in on every page load.
    """
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Redirects an unaurhtorize user to login page."""
    flash("Please sign in to continue.")
    return redirect(url_for("login_bp.login"))
