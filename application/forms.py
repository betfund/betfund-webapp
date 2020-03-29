from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class SignUpForm(FlaskForm):
    """
    Class to encapsulate sign up form
    """
    first_name = StringField(
        'First Name:',
        validators=[DataRequired()]
    )
    last_name = StringField(
        'Last Name:',
        validators=[DataRequired()]
    )
    email_address = StringField(
        'Email Address:',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField(
        'Password:',
        validators=[DataRequired()]
    )
    password_check = PasswordField(
        'Reenter Password:',
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
        'Email Address:',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField(
        'Password:',
        validators=[DataRequired()]
    )

    submit = SubmitField('Log In')
