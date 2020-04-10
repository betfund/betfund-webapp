from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class DepositForm(FlaskForm):
    """
    Class to encapsulate deposit form.
    """

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(message="Please enter an amount."),
            NumberRange(min=0, message="You cannot enter a negative amount."),
            NumberRange(max=10000, message="Maximum is $10,000."),
        ],
    )

    submit = SubmitField("Deposit")


class WithdrawForm(FlaskForm):
    """
    Class to encapsulate withdraw form.
    """

    amount = FloatField(
        "Amount",
        validators=[
            DataRequired(message="Please enter an amount."),
            NumberRange(min=0, message="You cannot enter a negative amount."),
        ],
    )

    submit = SubmitField("Withdraw")
