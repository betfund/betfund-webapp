import uuid
from datetime import datetime

from dateutil.parser import parse
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import and_, func

from application import db
from application.models import (
    Fund,
    FundLedger,
    FundUser,
    FundUserLedger,
    Strategy,
    User,
    UserLedger,
)
from application.views.funds.forms import CreateFundForm, InvestFundForm, JoinFundForm

funds_bp = Blueprint("funds_bp", __name__, template_folder="templates")


@funds_bp.app_template_filter('pretty_date')
def pretty_date(date, fmt='%b %d, %Y'):
    """Converts a date to pretty format.

    Parameters
    ----------
    date : datetime.datetime
        Datetime object for which to format.
    fmt : str
        String datetime format representation.

    Returns
    -------
    str
        Formatted datetime object as string.
    """
    if not date:
        return '-'
    return date.strftime(fmt)


@funds_bp.route("/dashboard/funds", methods=["GET", "POST"])
@login_required
def funds():
    """
    Funds route.
    TODO: This will be updated.
    """

    # initialize the deposit form
    create_fund_form = CreateFundForm()
    if request.method == "POST":

        # check to make sure the form is valid
        if create_fund_form.validate_on_submit():

            # get the form information
            fund_name = create_fund_form.fund_name.data
            fund_description = create_fund_form.fund_description.data
            sports = create_fund_form.strategy_sports.data
            solicitation_schedule = create_fund_form.strategy_solicitation_schedule.data
            solicitation_start = (
                create_fund_form.strategy_solicitation_schedule_start.data
            )
            solicitation_start = solicitation_start.isoformat()

            # create a strategy record
            strategy = Strategy(
                name=f"{fund_name} Strategy",
                code=str(uuid.uuid1()),
                details={
                    "sports": sports,
                    "solicitation_schedule": solicitation_schedule,
                    "solicitation_start": solicitation_start,
                },
            )
            db.session.add(strategy)
            db.session.commit()

            # create fund record
            fund = Fund(
                name=fund_name,
                description=fund_description,
                strategy_id=strategy.id,
                owner_id=current_user.id,
            )
            db.session.add(fund)
            db.session.commit()

            # add the owner as a fund user
            fund_user = FundUser(fund_id=fund.id, user_id=current_user.id)
            db.session.add(fund_user)
            db.session.commit()

            return redirect(url_for("funds_bp.funds"))

    # notify of any form errors
    for error_type, error_messages in create_fund_form.errors.items():
        for message in error_messages:
            flash(message)

    # get existing fund and relevant data
    fund_member_count_cte = (
        db.session.query(
            FundUser.fund_id.label("fund_id"),
            func.coalesce(func.count(FundUser.id), 0).label("member_count"),
        )
        .group_by(FundUser.fund_id)
        .cte("fund_member_count_cte")
    )
    fund_capital_size_cte = (
        db.session.query(
            FundLedger.fund_id.label("fund_id"),
            func.coalesce(func.sum(FundLedger.amount), 0).label("capital_size"),
        )
        .group_by(FundLedger.fund_id)
        .cte("fund_capital_size_cte")
    )
    fund_meta_cte = db.session.query(
        Fund.id.label("fund_id"),
        Fund.name,
        Fund.description,
        Fund.timestamp,
        Fund.owner_id,
    ).cte("fund_meta_cte")
    # finally combine all these common table expressions
    existing_funds = (
        db.session.query(
            fund_meta_cte.c.fund_id.label("id"),
            fund_meta_cte.c.name.label("name"),
            fund_meta_cte.c.description.label("description"),
            fund_meta_cte.c.timestamp.label("time_created"),
            fund_meta_cte.c.owner_id.label("owner_id"),
            fund_member_count_cte.c.member_count.label("member_count"),
            func.coalesce(fund_capital_size_cte.c.capital_size, 0).label("capital_size"),
        )
        .join(
            fund_member_count_cte,
            fund_member_count_cte.c.fund_id == fund_meta_cte.c.fund_id,
        )
        .outerjoin(
            fund_capital_size_cte,
            fund_capital_size_cte.c.fund_id == fund_meta_cte.c.fund_id,
        )
        .order_by(fund_capital_size_cte.c.capital_size.desc())
        .all()
    )

    return render_template(
        "funds/funds.html",
        title="Dashboard - Funds",
        user=current_user,
        form=create_fund_form,
        existing_funds=existing_funds,
    )


@funds_bp.route("/dashboard/funds/<int:fund_id>", methods=["GET", "POST"])
@login_required
def fund(fund_id):
    """
    Funds route.
    TODO: This will be updated.
    """

    invest_fund_form = InvestFundForm()
    join_fund_form = JoinFundForm()
    if request.method == "POST":

        if invest_fund_form.invest.data and invest_fund_form.validate_on_submit():
            """Returns the current users available balance."""
            available_balance = (
                db.session.query(func.coalesce(func.sum(UserLedger.amount), 0))
                .filter(UserLedger.user_id == current_user.id)
                .first()[0]
            )

            # get investment amount
            amount = invest_fund_form.amount.data

            # check whether the user has enough available capital
            if amount > available_balance:
                flash("You do not have sufficient funds available.")
                return redirect(url_for("funds_bp.fund", fund_id=fund_id))

            # keep one time stamp for future tracking
            timestamp = datetime.utcnow()

            # remove incoming investment from user available funds
            user_ledger = UserLedger(
                amount=(-amount), user_id=current_user.id, timestamp=timestamp
            )
            db.session.add(user_ledger)

            # insert money into the fund
            fund_ledger = FundLedger(
                amount=amount, timestamp=timestamp, fund_id=fund_id
            )
            db.session.add(fund_ledger)

            # get the fund user id of current user
            fund_user_id = (
                db.session.query(FundUser.id)
                .filter(
                    FundUser.fund_id == fund_id, FundUser.user_id == current_user.id
                )
                .first()[0]
            )
            # update the fund users ledger balance
            fund_user_ledger = FundUserLedger(
                amount=amount, timestamp=timestamp, fund_user_id=fund_user_id
            )
            db.session.add(fund_user_ledger)
            db.session.commit()

            return redirect(url_for("funds_bp.fund_success", fund_id=fund_id))

        if join_fund_form.join.data and join_fund_form.validate_on_submit():
            """Returns the current users available balance."""
            available_balance = (
                db.session.query(func.coalesce(func.sum(UserLedger.amount), 0))
                .filter(UserLedger.user_id == current_user.id)
                .first()[0]
            )

            # get investment amount
            amount = join_fund_form.amount.data

            # check whether the user has enough available capital
            if amount > available_balance:
                flash("You do not have sufficient funds available.")
                return redirect(url_for("funds_bp.fund", fund_id=fund_id))

            # keep one time stamp for future tracking
            timestamp = datetime.utcnow()

            # remove incoming investment from user available funds
            user_ledger = UserLedger(
                amount=(-amount), user_id=current_user.id, timestamp=timestamp
            )
            db.session.add(user_ledger)

            # insert member to fund
            fund_user = FundUser(fund_id=fund_id, user_id=current_user.id)
            db.session.add(fund_user)
            db.session.commit()

            # insert money into the fund
            fund_ledger = FundLedger(
                amount=amount, timestamp=timestamp, fund_id=fund_id
            )
            db.session.add(fund_ledger)

            # update the fund users ledger balance
            fund_user_ledger = FundUserLedger(
                amount=amount, timestamp=timestamp, fund_user_id=fund_user.id
            )
            db.session.add(fund_user_ledger)
            db.session.commit()

            return redirect(url_for("funds_bp.fund_success", fund_id=fund_id))

    # notify of any form errors
    for error_type, error_messages in invest_fund_form.errors.items():
        for message in error_messages:
            flash(message)

    # get fund information
    fund = (
        db.session.query(
            Fund.id.label("fund_id"),
            Fund.name.label("fund_name"),
            Fund.description.label("fund_description"),
            User.id.label("owner_id"),
            User.first_name.label("owner_first_name"),
            User.last_name.label("owner_last_name"),
            User.email_address.label("owner_email_address"),
            Strategy.id.label("strategy_id"),
            Strategy.name.label("strategy_name"),
            Strategy.code.label("strategy_code"),
            Strategy.details.label("strategy_details"),
        )
        .join(User, Fund.owner_id == User.id)
        .join(Strategy, Fund.strategy_id == Strategy.id)
        .filter(Fund.id == fund_id)
        .first()
    )

    # see if user is member of fund
    is_fund_member = db.session.query(
        db.exists().where(
            and_(FundUser.user_id == current_user.id, FundUser.fund_id == fund_id)
        )
    ).scalar()

    # see if user is owner of fund
    is_fund_owner = db.session.query(
        db.exists().where(and_(Fund.owner_id == current_user.id, Fund.id == fund_id))
    ).scalar()

    # get investment amount of current user in this fund
    fund_user_investment = (
        db.session.query(func.coalesce(func.sum(FundUserLedger.amount), 0))
        .join(FundUser, FundUser.id == FundUserLedger.fund_user_id)
        .join(User, FundUser.user_id == User.id)
        .join(Fund, FundUser.fund_id == Fund.id)
        .filter(User.id == current_user.id, Fund.id == fund_id)
        .first()[0]
    )

    return render_template(
        "funds/fund.html",
        title=f"Dashboard - {fund.fund_name} (#{fund.fund_id})",
        user=current_user,
        invest_form=invest_fund_form,
        join_form=join_fund_form,
        fund=fund,
        is_fund_member=is_fund_member,
        is_fund_owner=is_fund_owner,
        fund_user_investment=fund_user_investment,
    )


@funds_bp.route("/dashboard/funds/<int:fund_id>/success", methods=["GET"])
@login_required
def fund_success(fund_id):
    return redirect(url_for("funds_bp.fund", fund_id=fund_id))
