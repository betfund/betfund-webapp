from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__, template_folder='templates')


@home_bp.route('/', methods=['GET', 'POST'])
def home():
    """
    Homepage route.

    TODO :: This needs to be updated.
    """
    return render_template(
        'index.html',
        title='Home',
        template='template main',
        body="Home"
    )


@home_bp.route('/about', methods=['GET'])
def about():
    """
    About page route.

    TODO :: This needs to be updated.
    """
    return render_template(
        'index.html',
        title='About',
        template='template main',
        body="About"
    )
