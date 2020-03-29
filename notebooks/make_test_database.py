import argparse
import os
from random import choice, randint
from string import ascii_lowercase, ascii_uppercase, punctuation

import names

from application import create_app, db
from application.config import TestConfig
from application.models import User

POSSIBLE_CHARS = list(ascii_lowercase + ascii_uppercase + punctuation)


def make_fake_password(n_chars=10):
    """
    Generate a fake, random password. The password
    will start with an uppercase letter and end with
    a lowercase letter.

    Parameters
    ----------
    n_chars : int
        The number of characters (3, 20)
    """
    assert n_chars >= 3 and n_chars <= 20
    return ''.join([choice(ascii_uppercase)] +
                   [choice(POSSIBLE_CHARS) for _ in range(n_chars - 2)] +
                   [choice(ascii_lowercase)])


def make_user_test_data(n=20,
                        add_fake_admin=True,
                        password_chars_range=(8, 15)):
    """
    Make test user data

    Parameters
    ----------
    n : int
        The number of users.
        Defaults to 20.
    add_fake_admin : bool, optional
        Whether to add a fake admin user.
        Defaults to True.
    password_chars_range : 2-tuple, optional
        The range of possible password characters
        Defaults to (8, 15).
    """
    data = []
    start = 0
    if add_fake_admin:
        # add the fake admin user to the database
        data.append({'id': 0,
                     'first_name': 'Admin',
                     'last_name': 'User',
                     'email_address': 'admin@admin.com',
                     'password': 'admin'})
        start += 1

    for i in range(start, n + start):

        # get random email address form first initial and last name
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        email = choice(['@yahoo.com', '@gmail.com', '@aol.com'])
        email = ''.join([first_name.title(), last_name, email])

        # create a fake password
        password = make_fake_password(randint(password_chars_range[0],
                                              password_chars_range[1]))

        data.append({'id': i,
                     'first_name': first_name,
                     'last_name': last_name,
                     'email_address': email,
                     'password': password})

    return data


if __name__ == '__main__':

    # parse the arguments
    parser = argparse.ArgumentParser(prog='make_test_database')

    parser.add_argument('-n', dest='n', default=20,
                        help="The number of records to create.")

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Whether to print the records at the end.")

    # TODO :: Add other arguments?

    args = parser.parse_args()

    # remove the existing database
    if os.path.exists(TestConfig.db_path):
        os.remove(TestConfig.db_path)

    # create test data
    users = make_user_test_data(args.n)

    # create table
    app = create_app(test_config=True)
    db.create_all()

    # add the test data
    for user in users:

        # we'll want to hash the password
        password = user.pop('password')
        user = User(**user)
        user.set_password(password)
        db.session.add(user)

    db.session.commit()

    if args.verbose:
        print([{'id': u.id,
                'email': u.email_address,
                'pass': u.password} for u in User.query.all()])
