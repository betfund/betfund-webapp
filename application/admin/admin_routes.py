from flask import Blueprint, jsonify

from application.models import User
from flask_login import login_required

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')


@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    """
    Admin end point.

    TODO :: This DEFINITELY needs to be updated. We'll
    want to build out an actual admin end point with
    `flask_admin`, most likely. For now, this just
    returns all of the user data from the database.
    """
    users = User.query.all()
    users_json = [{
        'id': u.id,
        'first': u.first_name,
        'last': u.last_name,
        'email': u.email_address,
        'pass': u.password
    } for u in users]

    return jsonify(users_json)
