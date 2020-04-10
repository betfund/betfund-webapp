from datetime import datetime

from betfund_bet365 import Bet365SportId
from flask_wtf import FlaskForm
from wtforms import (
    DateTimeField,
    FloatField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.widgets import TextArea


class CreateFundForm(FlaskForm):
    """
    Class to encapsulate creating a fund
    """

    fund_name = StringField(
        "Fund name", validators=[DataRequired(message="Please specify a fund name.")]
    )

    fund_description = StringField(
        "Fund description",
        validators=[
            DataRequired(message="Please provide a fund description."),
            Length(min=10, message="Description must be minimum 40 characters."),
        ],
        widget=TextArea(),
    )

    strategy_sports = SelectMultipleField(
        "Which sports will this fund invest in?",
        choices=Bet365SportId.list(),
    )

    strategy_solicitation_schedule = SelectField(
        "How often will soliciation occur?",
        choices=[("hourly", "Hourly"), ("daily", "Daily"), ("weekly", "Weekly"),],
        validators=[DataRequired(message="Please select a solicitation schedule.")],
    )

    strategy_solicitation_schedule_start = DateTimeField(
        "When to start solicitations?",
        format="%b %d, %Y %H:%M:%S",
        default=datetime.utcnow,
    )

    submit = SubmitField("Create Fund")


class InvestFundForm(FlaskForm):
    """
    Class to encapsulate investing in a fund
    """

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(message="Please enter an amount."),
            NumberRange(min=0, message="You cannot enter a negative amount."),
        ],
    )

    invest = SubmitField("Invest")


class JoinFundForm(FlaskForm):
    """
    Class to encapsulate investing in a fund
    """

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(message="Please enter an amount."),
            NumberRange(min=0, message="You cannot enter a negative amount."),
        ],
    )

    join = SubmitField("Join")
