from flask import Blueprint, flash, redirect, url_for
from flask_mail import Message

from application import mail

survey_bp = Blueprint("survey_bp", __name__, template_folder="templates")


@survey_bp.route("/dashboard/surveys", methods=["GET"])
def surveys():
    msg = Message(
        "Hello World",
        sender=("Betfund", "survey@betfund.com"),
        recipients=["mitchbregs@gmail.com"],
    )
    mail.send(msg)

    return redirect(url_for("home_bp.home"))
