from flask import Blueprint, render_template
from flask_login import login_required

loggedin_bp = Blueprint('loggedin_bp', __name__, template_folder='templates')


@loggedin_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Dashboard route.

    TODO :: This will be updated.
    """
    return render_template(
        'dashboard.html',
        title='Dashboard',
        template='template main',
        body="Dashboard"
    )
