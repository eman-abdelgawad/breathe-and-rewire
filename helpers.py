import requests

from flask import redirect, render_template, session, request
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    return render_template("apology.html", top=code, bottom=message), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# Validates a form field must be a non-negative integer, returns that int or None
def validate_field(name):
    try:
        value = request.form.get(name)

        if value is None or value == "":
            return None

        value = int(value)
        if value < 0:
            return None
        return value

    except (ValueError, TypeError):
        return None


