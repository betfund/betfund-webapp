from flask_admin.contrib.sqla import ModelView

from application import db
from application.models import (
    Fund,
    FundLedger,
    FundUser,
    FundUserLedger,
    Investment,
    Line,
    LineVote,
    Result,
    Strategy,
    User,
    UserLedger
)
from flask_login import login_required


def add_admin_views(administrator):
    """Register views to admin"""
    administrator.add_view(ModelView(Fund, session=db.session, name='Fund'))
    administrator.add_view(ModelView(FundLedger, session=db.session, name='FundLedger'))
    administrator.add_view(ModelView(FundUser, session=db.session, name='FundUser'))
    administrator.add_view(ModelView(FundUserLedger, session=db.session, name='FundUserLedger'))
    administrator.add_view(ModelView(Investment, session=db.session, name='Investment'))
    administrator.add_view(ModelView(Line, session=db.session, name='Line'))
    administrator.add_view(ModelView(LineVote, session=db.session, name='LineVote'))
    administrator.add_view(ModelView(Result, session=db.session, name='Result'))
    administrator.add_view(ModelView(Strategy, session=db.session, name='Strategy'))
    administrator.add_view(ModelView(User, session=db.session, name='User'))
    administrator.add_view(ModelView(UserLedger, session=db.session, name='UserLedger'))
