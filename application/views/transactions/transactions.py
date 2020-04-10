from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from application import db
from application.models import Fund, FundUser, FundUserLedger, User, UserLedger

transactions_bp = Blueprint("transactions_bp", __name__, template_folder="templates")


@transactions_bp.route("/dashboard/transactions", methods=["GET"])
@login_required
def transactions():
    """
    Transactions route.

    GET:    Return transactions for a given user.
    """

    # gets current users deposits and withdrawals
    user_transactions = (
        db.session.query(UserLedger.id, UserLedger.timestamp, UserLedger.amount)
        .filter(UserLedger.user_id == current_user.id)
        .order_by(UserLedger.timestamp.asc())
        .all()
    )

    # gets current users fund transactions
    fund_user_transactions = (
        db.session.query(
            FundUserLedger.id,
            FundUserLedger.timestamp,
            Fund.name,
            FundUserLedger.amount,
        )
        .join(FundUser, FundUserLedger.fund_user_id == FundUser.id)
        .join(User, FundUser.user_id == User.id)
        .join(Fund, FundUser.fund_id == Fund.id)
        .filter(User.id == current_user.id)
        .order_by(FundUserLedger.timestamp.asc())
        .all()
    )

    return render_template(
        "transactions/transactions.html",
        title="Transactions",
        user=current_user,
        user_transactions=user_transactions,
        fund_user_transactions=fund_user_transactions,
    )
