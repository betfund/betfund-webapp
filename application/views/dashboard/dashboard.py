from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import func

from application import db
from application.models import FundUser, FundUserLedger, User, UserLedger
from application.views.dashboard.forms import DepositForm

dashboard_bp = Blueprint("dashboard_bp", __name__, template_folder="templates")


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    """
    Dashboard route.

    TODO: This will be updated.
    """

    # initialize the deposit form
    deposit_form = DepositForm()
    if request.method == "POST":

        # check to make sure the form is valid
        if deposit_form.validate_on_submit():

            # get the amount to deposit
            amount = deposit_form.amount.data

            # create a user ledger record
            deposit = UserLedger(amount=amount, user_id=current_user.id)

            # persist to user ledger table
            db.session.add(deposit)
            db.session.commit()

            return redirect(url_for("dashboard_bp.dashboard"))

    # notify of any form errors
    for error_type, error_messages in deposit_form.errors.items():
        for message in error_messages:
            flash(message)

    # available balance
    available_balance = (
        db.session.query(func.coalesce(func.sum(UserLedger.amount), 0))
        .filter(UserLedger.user_id == current_user.id)
        .first()[0]
    )

    # invested into funds balance
    invested_balance = (
        db.session.query(func.coalesce(func.sum(FundUserLedger.amount), 0))
        .join(FundUser, FundUserLedger.fund_user_id == FundUser.id)
        .join(User, FundUser.user_id == User.id)
        .filter(User.id == current_user.id)
        .first()[0]
    )

    return render_template(
        "dashboard/dashboard.html",
        title="Dashboard",
        user=current_user,
        form=deposit_form,
        available_balance=available_balance,
        invested_balance=invested_balance,
    )
