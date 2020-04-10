from flask import Blueprint, flash, redirect, render_template, url_for

from application import db
from application.models import User
from application.views.auth import SignupForm

signup_bp = Blueprint("signup_bp", __name__, template_folder="templates")


@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    """
    End point for sign up page.

    GET:    Returns the sign up page.
    POST:   Attempts signup.
                If fail, redirect and display errors.
                If success, redirect to signup succes page.
    """

    signup_form = SignupForm()
    if signup_form.validate_on_submit():

        # get the form data, if submission was valid
        first_name = signup_form.first_name.data
        last_name = signup_form.last_name.data
        email_address = signup_form.email_address.data
        password = signup_form.password.data

        # check to see if this user already exists in the database
        if User.query.filter_by(email_address=email_address).first() is None:

            # if not, then add them to the database, but make
            # sure to hash the password that was entered ...
            user = User(
                first_name=first_name, last_name=last_name, email_address=email_address
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # if this is successful, redirect to the success page
            return redirect(url_for("signup_bp.success"))

        # otherwise, let them know a user already exists with this email
        flash("A user already exists with that email address.")
        return redirect(url_for("signup_bp.signup"))

    # notify of any form errors
    for error_type, error_messages in signup_form.errors.items():
        for message in error_messages:
            flash(message)

    return render_template("auth/signup_form.html", form=signup_form, title="Sign Up")


@signup_bp.route("/success", methods=["GET"])
def success():
    """
    End point for successful sign up.
    """
    return render_template("auth/signup_success.html")
