import datetime
import json
import uuid

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import func

from application import db, login_manager
from application.forms import (
    CreateFundForm,
    DepositForm,
    InvestFundForm,
    SearchForm
)
from application.models import (
    Fund,
    FundLedger,
    FundUser,
    FundUserLedger,
    Strategy,
    User,
    UserLedger
)

loggedin_bp = Blueprint('loggedin_bp', __name__, template_folder='templates')


@login_manager.unauthorized_handler
def unauthorized_callback():
    """Redirects an unaurhtorize user to login page."""
    flash('Please sign in to continue.')
    return redirect(url_for('login_bp.login'))


@loggedin_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """
    Dashboard route.

    TODO: This will be updated.
    """

    # available balance
    available_balance = db.session.query(
        func.coalesce(func.sum(UserLedger.amount), 0)
    ).filter(
        UserLedger.user_id == current_user.id
    ).first()[0]

    # invested into funds balance
    invested_balance = db.session.query(
        func.coalesce(func.sum(FundUserLedger.amount), 0)
    ).join(
        FundUser,
        FundUserLedger.fund_user_id == FundUser.id
    ).join(
        User,
        FundUser.user_id == User.id
    ).filter(
        User.id == current_user.id
    ).first()[0]

    # initialize the deposit form
    deposit_form = DepositForm()
    if request.method == 'POST':

        # check to make sure the form is valid
        if deposit_form.validate_on_submit():

            # get the amount to deposit
            amount = deposit_form.amount.data

            # create a user ledger record
            deposit = UserLedger(amount=amount, user_id=current_user.id)

            # persist to user ledger table
            db.session.add(deposit)
            db.session.commit()

            return redirect(url_for('loggedin_bp.dashboard'))

    # notify of any form errors
    for error_type, error_messages in deposit_form.errors.items():
        for message in error_messages:
            flash(message)

    return render_template(
        'dashboard-home.html',
        title='Dashboard',
        user=current_user,
        form=deposit_form,
        available_balance=available_balance,
        invested_balance=invested_balance
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
        FundUserLedger.timestamp.asc()
    ).all()

    return render_template(
        'dashboard-transactions.html',
        title='Transactions',
        user=current_user,
        user_transactions=user_transactions,
        fund_user_transactions=fund_user_transactions
    )


@loggedin_bp.route('/dashboard/funds', methods=['GET', 'POST'])
@login_required
def funds():
    """
    Funds route.

    TODO: This will be updated.
    """

    # get existing funds
    existing_funds = db.session.query(
        Fund.id,
        Fund.name,
        Fund.description,
        Fund.strategy_id,
        Fund.owner_id,
        func.coalesce(func.count(FundUser.id), 0).label('fund_member_count')
    ).join(
        FundUser,
        FundUser.fund_id == Fund.id,
    ).group_by(
        Fund.id
    ).all()

    # initialize the deposit form
    create_fund_form = CreateFundForm()
    if request.method == 'POST':

        # check to make sure the form is valid
        if create_fund_form.validate_on_submit():

            # get the form information
            fund_name = create_fund_form.fund_name.data
            fund_description = create_fund_form.fund_description.data
            sports = create_fund_form.strategy_sports.data
            solicitation_schedule = create_fund_form.strategy_solicitation_schedule.data
            solicitation_start = create_fund_form.strategy_solicitation_schedule_start.data
            solicitation_start = solicitation_start.isoformat()

            # create a strategy record
            strategy = Strategy(
                name=f"{fund_name} Strategy",
                code=str(uuid.uuid1()),
                details={
                        "sports": sports,
                        "solicitation_schedule": solicitation_schedule,
                        "solicitation_start": solicitation_start
                }
            )
            db.session.add(strategy)
            db.session.commit()

            # create fund record
            fund = Fund(
                name=fund_name,
                description=fund_description,
                strategy_id=strategy.id,
                owner_id=current_user.id
            )
            db.session.add(fund)
            db.session.commit()

            fund_user = FundUser(
                fund_id=fund.id,
                user_id=current_user.id
            )
            db.session.add(fund_user)
            db.session.commit()

            return redirect(url_for('loggedin_bp.funds'))

    # notify of any form errors
    for error_type, error_messages in create_fund_form.errors.items():
        for message in error_messages:
            flash(message)

    return render_template(
        'dashboard-funds.html',
        title='Dashboard - Funds',
        user=current_user,
        form=create_fund_form,
        existing_funds=existing_funds
    )


@loggedin_bp.route('/dashboard/funds/<int:fund_id>', methods=['GET', 'POST'])
@login_required
def fund(fund_id):
    """
    Funds route.

    TODO: This will be updated.
    """

    invest_fund_form = InvestFundForm()
    if request.method == 'POST':

        """Returns the current users available balance."""
        available_balance = db.session.query(
            func.coalesce(func.sum(UserLedger.amount), 0)
        ).filter(
            UserLedger.user_id == current_user.id
        ).first()[0]

        # get investment amount
        amount = invest_fund_form.amount.data

        # check whether the user has enough available capital
        if amount > available_balance:
            flash('You do not have sufficient available funds.')
            return redirect(url_for('loggedin_bp.fund', fund_id=fund_id))

        timestamp = datetime.datetime.utcnow().replace(microsecond=0)

        # remove incoming investment from user available funds
        user_ledger = UserLedger(
            amount=(-amount),
            user_id=current_user.id,
            timestamp=timestamp
        )
        db.session.add(user_ledger)

        # insert money into the fund
        fund_ledger = FundLedger(
            amount=amount,
            timestamp=timestamp,
            fund_id=fund_id
        )
        db.session.add(fund_ledger)

        # get the fund user id of current user
        fund_user_id = db.session.query(
            FundUser.id
        ).filter(
            FundUser.fund_id == fund_id,
            FundUser.user_id == current_user.id
        ).first()[0]
        # update the fund users ledger balance
        fund_user_ledger = FundUserLedger(
            amount=amount,
            timestamp=timestamp,
            fund_user_id=fund_user_id
        )
        db.session.add(fund_user_ledger)
        db.session.commit()

        redirect(url_for('loggedin_bp.fund', fund_id=fund_id))

    # notify of any form errors
    for error_type, error_messages in invest_fund_form.errors.items():
        for message in error_messages:
            flash(message)

    # get fund information
    fund = db.session.query(
        Fund.id.label('fund_id'),
        Fund.name.label('fund_name'),
        Fund.description.label('fund_description'),
        User.id.label('owner_id'),
        User.first_name.label('owner_first_name'),
        User.last_name.label('owner_last_name'),
        User.email_address.label('owner_email_address'),
        Strategy.id.label('strategy_id'),
        Strategy.name.label('strategy_name'),
        Strategy.code.label('strategy_code'),
        Strategy.details.label('strategy_details'),
        func.coalesce(func.count(FundUser.id), 0).label('fund_member_count')
    ).join(
        User,
        Fund.owner_id == User.id
    ).join(
        Strategy,
        Fund.strategy_id == Strategy.id
    ).join(
        FundUser,
        FundUser.fund_id == Fund.id
    ).filter(
        Fund.id == fund_id
    ).first()

    # get investment amount of current user in this fund
    fund_user_investment = db.session.query(
        func.coalesce(func.sum(FundUserLedger.amount), 0)
    ).join(
        FundUser,
        FundUser.id == FundUserLedger.fund_user_id
    ).join(
        User,
        FundUser.user_id == User.id
    ).join(
        Fund,
        FundUser.fund_id == Fund.id
    ).filter(
        User.id == current_user.id,
        Fund.id == fund_id
    ).first()[0]

    return render_template(
        'dashboard-fund.html',
        title=f'Dashboard - {fund.fund_name} (#{fund.fund_id})',
        user=current_user,
        form=invest_fund_form,
        fund=fund,
        fund_user_investment=fund_user_investment
    )
