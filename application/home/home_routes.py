from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user

home_bp = Blueprint('home_bp', __name__, template_folder='templates')


@home_bp.route('/', methods=['GET'])
def home():
    """
    Homepage route.

    GET:    Redirects user to their dashboard if they are already logged in.
    """

    # redirect a user to their dashboard
    # if they are alreday logged in
    if current_user.is_authenticated:
        return redirect(url_for('loggedin_bp.dashboard'))

    return render_template(
        'index.html',
        title='Home',
    )


@home_bp.route('/about', methods=['GET'])
def about():
    """
    About page route.

    TODO: This needs to be updated.
    """
    return render_template(
        'index.html',
        title='About',
    )
