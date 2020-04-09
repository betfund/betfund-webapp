from flask_login import UserMixin
from sqlalchemy.sql import func
from werkzeug.security import check_password_hash, generate_password_hash

from application import db


class User(db.Model, UserMixin):
    """
    SQLAlchemy object :: `users` table.

    Fields
    ------
    id : int
        The primary key and user identifier.
    first_name : str
        The given name of user.
    last_name : str
        The family name of user.
    email_address : str
        The user"s email address.
    password : str
        The user password. This should be hashed.
    created_on : datetime
        When was the user created.
    modified_on : str
        When was the user information modified.
    role : str
        Optional. Only instantiated upon verification of user or admin.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(10), nullable=True)
    email_address = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), default=func.now())
    modified_on = db.Column(db.DateTime(timezone=True), default=func.now())
    role = db.Column(db.String(16), nullable=True)

    def set_password(self, password):
        """
        Create hashed password.
        """
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """
        Check hashed password.
        """
        return check_password_hash(self.password, password)

    @property
    def is_confirmed(self):
        """
        Check if user is verified.
        """
        return self.role == 'admin' or self.role == 'user'

    @property
    def is_new(self):
        """
        Check if user is new with unverified account.
        """
        return self.role == None

    @property
    def is_user(self):
        """
        Check if verified user.
        """
        return self.role == 'user'

    def __repr__(self):
        return f"<User `{self.id}`>"


class UserLedger(db.Model):
    """
    SQLAlchemy object :: `user_ledgers` table.

    Fields
    ------
    id : int
        The primary key and user identifier.
    user_id : int
        The user identifier.
    amount : float
        Transaction value.
    timestamp : datetime
        Timestamp of transaction.
    """

    __tablename__ = "user_ledgers"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    # relationships
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship('User', backref=db.backref('userledger', lazy='dynamic'))

    def __repr__(self):
        return f"<UserLedger `{self.id}`>"


class FundUser(db.Model):
    """
    SQLAlchemy object :: `fund_users` table.

    Represents a lookup table for which users belong to what funds. A user
    can be a member of multiple funds. There exists a unique index on the
    combination of a user and a fund.

    Fields
    ------
    id : int
        The primary key and fund user identifier.
    fund_id : int
        The fund identifier.
    user_id : int
        The user identifier.
    """

    __tablename__ = "fund_users"
    __table_args__ = (
        db.UniqueConstraint('fund_id', 'user_id', name='unique_idx_fund_id_user_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # relationships
    fund_id = db.Column(db.Integer, db.ForeignKey("funds.id"), nullable=False)
    fund = db.relationship('Fund', backref=db.backref('funduser', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship('User', backref=db.backref('funduser', lazy='dynamic'))

    def __repr__(self):
        return f"<FundUser `{self.id}`>"


class Line(db.Model):
    """
    SQLAlchemy object :: `lines` table.

    Represents a table containing betting lines.

    Fields
    ------
    id : str
        The primary key and line identifier.
    details : dict
        All metadata around an event betting line.
    """

    __tablename__ = "lines"

    id = db.Column(db.String(64), primary_key=True)
    details = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Line `{self.id}`>"


class LineVote(db.Model):
    """
    SQLAlchemy object :: `line_votes` table.

    Represents a table containing votes placed by fund users on which
    lines to take on a given day.

    Fields
    ------
    id : int
        The primary key and line vote identifier.
    line_id : str
        The line identifier.
    fund_user_id : int
        The fund user identifier.
    units : int
        Weight of vote.
    timestamp : datetime
        Timestamp of vote.
    """

    __tablename__ = "line_votes"

    id = db.Column(db.Integer, primary_key=True)
    units = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=True)

    # relationships
    line_id = db.Column(db.String(64), db.ForeignKey("lines.id"), nullable=False)
    fund_user_id = db.Column(db.Integer, db.ForeignKey("fund_users.id"), nullable=False)

    def __repr__(self):
        return f"<LineVote `{self.id}`>"


class FundUserLedger(db.Model):
    """
    SQLAlchemy object :: `fund_user_ledgers` table.

    Fields
    ------
    id : int
        The primary key and fund user ledger identifier.
    fund_user_id : int
        The fund user identifier.
    amount : float
        Transaction value.
    timestamp : datetime
        Timestamp of transaction.
    """

    __tablename__ = "fund_user_ledgers"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    # relationships
    fund_user_id = db.Column(db.Integer, db.ForeignKey("fund_users.id"), nullable=False)
    fund_user = db.relationship('FundUser', backref=db.backref('funduserledger', lazy='dynamic'))

    def __repr__(self):
        return f"<FundUserLedger `{self.id}`>"


class FundLedger(db.Model):
    """
    SQLAlchemy object :: `fund_ledger` table.

    Fields
    ------
    id : int
        The primary key and fund ledger identifier.
    fund_id : int
        The fund identifier.
    amount : float
        Transaction value.
    timestamp : datetime
        Timestamp of transaction.
    """

    __tablename__ = "fund_ledgers"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    # relationships
    fund_id = db.Column(db.Integer, db.ForeignKey("funds.id"), nullable=False)
    fund = db.relationship('Fund', backref=db.backref('fundledger', lazy='dynamic'))

    def __repr__(self):
        return f"<FundLedger `{self.id}`>"


class Fund(db.Model):
    """
    SQLAlchemy object :: `funds` table.

    Fields
    ------
    id : int
        The primary key and fund identifier.
    name : str
        The given name of fund.
    """

    __tablename__ = "funds"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(516), nullable=False)

    # relationships
    strategy_id = db.Column(db.Integer, db.ForeignKey("strategies.id"), nullable=False)
    strategy = db.relationship('Strategy', backref=db.backref('fund', lazy='dynamic'))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship('User', backref=db.backref('fund', lazy='dynamic'))

    def __repr__(self):
        return f"<Fund `{self.id}`>"


class Strategy(db.Model):
    """
    SQLAlchemy object :: "strategies" table.

    Fields
    ------
    id : int
        The primary key and strategy identifier.
    name : str
        The name of a strategy.
    code : str
        The code for a strategy.
    definition : dict
        The strategy definition.
    """

    __tablename__ = "strategies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    code = db.Column(db.String(128), nullable=False, unique=True)
    details = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return f"<Strategy `{self.id}`>"


class Investment(db.Model):
    """
    SQLAlchemy object :: "investments" table.

    Fields
    ------
    id : int
        The primary key and investment identifier.
    fund_id : str
        The fund identifier.
    line_id : str
        The line identifier.
    amount : float
        Transaction value.
    timestamp : datetime
        Timestamp of transaction.
    """

    __tablename__ = "investments"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    # relationships
    fund_id = db.Column(db.Integer, db.ForeignKey("funds.id"), nullable=False)
    line_id = db.Column(db.String(64), db.ForeignKey("lines.id"), nullable=False)

    def __repr__(self):
        return f"<Investment `{self.id}`>"


class Survey(db.Model):
    """
    SQLAlchemy object :: "surveys" table.

    Fields
    ------
    id : int
        The primary key and survey identifier.
    start_time : datetime
        Time when survey goes live.
    end_time : datetime
        Time when survey ends.
    fund_id : int
        The fund identifier.
    """

    __tablename__ = "surveys"

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))

    # relationships
    fund_id = db.Column(db.Integer, db.ForeignKey("funds.id"), nullable=False)


class Result(db.Model):
    """
    SQLAlchemy object :: "results" table.

    Fields
    ------
    id : int
        The primary key and result identifier.
    investment_id : int
        The investment identifier.
    amount : float
        Transaction value.
    is_win : bool
        Did the bet win?
    """

    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    is_win = db.Column(db.Boolean, nullable=False)

    # relationships
    investment_id = db.Column(db.Integer, db.ForeignKey("investments.id"), nullable=False)

    def __repr__(self):
        return f"<Result `{self.id}`>"
