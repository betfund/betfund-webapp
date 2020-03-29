from flask import Blueprint, flash, redirect, render_template, url_for

from application.forms import SignUpForm
from application.models import User, db

signup_bp = Blueprint('signup_bp', __name__, template_folder='templates')


@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    End point for sign up page.
    """
    form = SignUpForm()
    if form.validate_on_submit():

        # get the form data, if submission was valid
        first_name = form.first_name.data
        last_name = form.last_name.data
        email_address = form.email_address.data
        password = form.password.data

        # check to see if this user already exists in the database
        if User.query.filter_by(email_address=email_address).first() is None:
 
            # if not, then add them to the database, but make
            # sure to hash the password that was entered ...
            user = User(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # if this is successful, redirect to the success page
            return redirect(url_for('signup_bp.success'))

        # otherwise, let them know a user already exists with this email
        flash('A user already exists with that email address.')
        return redirect(url_for('signup_bp.signup'))

    return render_template(
        'signup_form.html',
        form=form,
        template='template main',
        body="Register"
    )


@signup_bp.route('/success', methods=['GET'])
def success():
    """
    End point for successful sign up.
    """
    return render_template('signup_success.html', template='template main')
