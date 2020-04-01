from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from application import db, login_manager
from application.forms import SearchForm
from application.models import Fund, FundUser, FundUserLedger, User, UserLedger

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

    return render_template(
        'dashboard-home.html',
        title='Dashboard',
        user=current_user
    )


@loggedin_bp.route('/dashboard/transactions', methods=['GET'])
@login_required
def transactions():
    """
    Dashboard route.

    TODO: This will be updated.
    """

    # gets current users deposits and withdrawals
    user_transactions = db.session.query(
        UserLedger.id,
        UserLedger.timestamp,
        UserLedger.amount
    ).filter(
        UserLedger.user_id == current_user.id
    ).order_by(
        UserLedger.timestamp.asc()
    ).all()

    
    # gets current users fund transactions
    fund_user_transactions = db.session.query(
        FundUserLedger.id,
        FundUserLedger.timestamp,
        Fund.name,
        FundUserLedger.amount
    ).join(
        FundUser,
        FundUserLedger.fund_user_id == FundUser.id
    ).join(
        User,
        FundUser.user_id == User.id
    ).join(
        Fund,
        FundUser.fund_id == Fund.id
    ).filter(
        User.id == current_user.id
    ).order_by(
        Fund.name,
        FundUserLedger.timestamp.asc()
    ).all()

    return render_template(
        'dashboard-transactions.html',
        title='Transactions',
        user=current_user,
        user_transactions=user_transactions,
        fund_user_transactions=fund_user_transactions
    )

