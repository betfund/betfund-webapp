from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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
        validators=[DataRequired("Please enter your search terms.")]
    )