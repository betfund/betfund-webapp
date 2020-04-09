from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy.sql import func
from wtforms import (
    DateTimeField,
    FloatField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms.widgets import TextArea

from application import db
from application.models import UserLedger


class SignUpForm(FlaskForm):
    """
    Class to encapsulate sign up form
    """
    first_name = StringField(
        'First name',
        validators=[DataRequired(message="Please enter your first name.")]
    )
    last_name = StringField(
        'Last name',
        validators=[DataRequired(message="Please enter your last name.")]
    )
    email_address = StringField(
        'Email address',
        validators=[
            DataRequired(message="Please enter an email."),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Please enter a password."),
            Length(min=8, max=24, message="Password must be between 8 and 24 characters.")
        ]
    )
    password_check = PasswordField(
        'Re-enter password',
        validators=[
            DataRequired(message="Please re-enter a password."),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    """
    Class to encapsulate log in form
    """
    email_address = StringField(
        'Email address',
        validators=[
            DataRequired(message="Please enter your email."),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message="Please enter your password.")]
    )

    submit = SubmitField('Log In')


class SearchForm(FlaskForm):
    """
    Class to encapsulate search form
    """
    text = StringField(
        'Search terms',
        validators=[DataRequired(message="Please enter your search terms.")]
    )


class DepositForm(FlaskForm):
    """
    Class to encapsulate deposit form
    """
    amount = FloatField(
        'Amount',
        validators=[
            DataRequired(message="Please enter an amount."),
            NumberRange(min=0, message="You cannot enter a negative amount."),
            NumberRange(max=1000, message="Maximum is $1000.")
        ]
    )

    submit = SubmitField('Deposit')


class CreateFundForm(FlaskForm):
    """
    Class to encapsulate creating a fund
    """
    fund_name = StringField(
        'Fund name',
        validators=[DataRequired(message="Please specify a fund name.")]
    )

    fund_description = StringField(
        'Fund description',
        validators=[
            DataRequired(message="Please provide a fund description."),
            Length(min=10, message="Description must be minimum 40 characters.")
        ],
        widget=TextArea()
    )

    # replace this with betfund-bet365 enumeration later
    strategy_sports = SelectMultipleField(
        'Which sports will this fund invest in?',
        choices=[
            ('1', 'National Football League'),
            ('2', 'National Basketball Association'),
            ('3', 'National Hockey League'),
            ('4', 'Major League Baseball'),
            ('5', 'Russian Premier League'),
            ('6', 'eSports')
        ]
    )

    strategy_solicitation_schedule = SelectField(
        'How often will soliciation occur?',
        choices=[
            ('hourly', 'Hourly'),
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
        ],
        validators=[DataRequired(message="Please select a solicitation schedule.")]
    )

    strategy_solicitation_schedule_start = DateTimeField(
        'When to start solicitations?',
        format="%b/%d/%Y %H:%M:%S",
        default=datetime.utcnow
    )

    submit = SubmitField('Create Fund')


class InvestFundForm(FlaskForm):
    """
    Class to encapsulate investing in a fund
    """

    amount = FloatField(
        'Amount',
        validators=[
            DataRequired(message="Please enter an amount."),
            NumberRange(min=0, message="You cannot enter a negative amount."),
        ]
    )

    submit = SubmitField('Invest')

