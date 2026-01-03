import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, validate_field

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///breathwork.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    default_breathworks = db.execute(
        "SELECT * FROM breathworks WHERE is_default = 1")
    custom_breathworks = db.execute(
        "SELECT * FROM breathworks WHERE is_default = 0 AND user_id = ?", session["user_id"])

    return render_template("index.html", default_breathworks=default_breathworks, custom_breathworks=custom_breathworks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # TODO

    if request.method == "POST":
        user_name = request.form.get("username")

        # check user_name
        if not user_name:
            return apology("Missing user name", 400)
        user_name_check = db.execute("SELECT * FROM users WHERE username = ?", user_name)
        if user_name_check:
            return apology("The username already exists", 400)

        # password
        password = request.form.get("password")
        if not password:
            return apology("Missing password", 400)

        confirmation = request.form.get("confirmation")
        if not confirmation:
            return apology("Missing confirmation", 400)

        if password != confirmation:
            return apology("Password and confirmation are not matching.", 400)

        password_hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES(?,?)", user_name, password_hash)
        except ValueError:
            return apology("The username already exists", 409)

        flash("Registered!")
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        old_password = request.form.get("oldpassword")
        new_password = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")

        # check old password hash as if it is login
        if not old_password:
            return apology("must provide the old password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], old_password
        ):
            return apology("invalid old password", 403)

        # check the match of password and confirmation
        if not new_password:
            return apology("must provide a NEW password", 403)
        if not confirmation:
            return apology("must provide a confirmation for the NEW password", 403)

        if new_password != confirmation:
            return apology("The confirmation and the NEW password are not matching", 403)

        # update the DB with the new hash
        password_hash = generate_password_hash(new_password)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", password_hash, session["user_id"])

        return redirect("/login")

    return render_template("settings.html")


@app.route("/editor", methods=["GET", "POST"])
@login_required
def editor():
    if request.method == "GET":
        breathworks = db.execute(
            "SELECT * FROM breathworks WHERE is_default = 0 AND user_id=?", session["user_id"])
        return render_template("editor.html", breathworks=breathworks)

    # insert the new breathwork, must have a unique name, no redundant breathwork's name for each user
    if request.method == "POST":
        name = request.form.get("name")

        # check breathwork's name in user custom breathwork
        # search in DB by breathwork's name instead of retrieving all user's breathworks and search here
        breathwork = db.execute(
            "SELECT * FROM breathworks WHERE is_default = 0 AND user_id=? AND name =?", session["user_id"], name)

        if breathwork:
            return jsonify(success=False, message="You already have a breathwork with this name, Please enter a different name or edit the existing one in table below"), 400

        description = request.form.get("description")
        if len(description) > 100:
            return jsonify(success=False, message="Your description is too long. Please keep it within 100 characters."), 400

        inhale = validate_field("inhale")
        print(inhale)
        if inhale is None:
            return jsonify(success=False, message="Inhale must be an integer 0 or greater."), 400

        inhale_hold = validate_field("inhale_hold")
        print(inhale_hold)
        if inhale_hold is None:
            return jsonify(success=False, message="Inhale hold must be an integer 0 or greater."), 400

        exhale = validate_field("exhale")
        print(exhale)
        if exhale is None:
            return jsonify(success=False, message="Exhale must be an integer 0 or greater."), 400

        exhale_hold = validate_field("exhale_hold")
        print(exhale_hold)
        if exhale_hold is None:
            return jsonify(success=False, message="Exhale Hold must be an integer 0 or greater."), 400

        rounds = validate_field("rounds")
        if rounds is None or rounds == 0:
            return jsonify(success=False, message="Rounds must be an integer number greater than 0. At least breathe for 1 round!"), 400

        try:
            new_breathwork_id = db.execute("INSERT INTO breathworks (name,description,inhale,inhale_hold,exhale,exhale_hold,rounds,user_id) VALUES(?,?,?,?,?,?,?,?)",
                                           name, description, inhale, inhale_hold, exhale, exhale_hold, rounds, session["user_id"])

            new_breathwork = db.execute(
                "SELECT * FROM breathworks WHERE id=?", new_breathwork_id)
            return jsonify(success=True, new_breathwork=new_breathwork[0])

        except Exception as e:
            return jsonify(success=False, message="Failed to add this breathwork"), 400


@app.route("/history")
@login_required
def history():
    breathwork_logs = db.execute(
        "SELECT breathworks.name, logs.id, logs.log_date, logs.duration_seconds, logs.notes FROM logs JOIN breathworks ON logs.breathwork_id = breathworks.id WHERE logs.user_id = ?", session["user_id"])

    # change "duration_seconds" to minutes and seconds the list of dict "breathwork_logs"
    # change the time from UTC (default) to the user's timezone, I did it in js to get the user's timezone dynamically
    for log in breathwork_logs:
        duration = int(log["duration_seconds"])
        log["minutes"] = duration // 60
        log["seconds"] = duration % 60
    return render_template("history.html", breathwork_logs=breathwork_logs)


@app.route("/delete-log/<int:log_id>", methods=["DELETE"])
@login_required
def delete_log(log_id):
    db.execute("DELETE FROM logs WHERE id = ?", log_id)
    return ("", 204)


@app.route("/delete-breathwork/<int:breathwork_id>", methods=["DELETE"])
@login_required
def delete_breathwork(breathwork_id):
    db.execute("DELETE FROM breathworks WHERE id = ?", breathwork_id)
    return ("", 204)


@app.route("/edit-breathwork/<int:breathwork_id>", methods=["GET", "POST"])
@login_required
def edit_breathwork(breathwork_id):
    # show the form filled with old values
    if request.method == "GET":
        breathwork = db.execute(
            "SELECT id,name,description,inhale,inhale_hold,exhale,exhale_hold,rounds FROM breathworks WHERE user_id = ? AND id = ?", session["user_id"], breathwork_id)
        if not breathwork:
            return apology("Breathwork not found.", 404)
        return render_template("edit-breathwork.html", breathwork=breathwork[0])

    # pull form data and update DB
    if request.method == "POST":
        name = request.form.get("name")

        description = request.form.get("description")
        if len(description) > 100:
            return apology("Your description is too long. Please keep it within 100 characters.", 400)

        inhale = validate_field("inhale")
        print(inhale)
        if inhale is None:
            return apology("Inhale must be an integer 0 or greater.", 400)

        inhale_hold = validate_field("inhale_hold")
        print(inhale_hold)
        if inhale_hold is None:
            return apology("Inhale hold must be an integer 0 or greater.", 400)

        exhale = validate_field("exhale")
        print(exhale)
        if exhale is None:
            return apology("Exhale must be an integer 0 or greater.", 400)

        exhale_hold = validate_field("exhale_hold")
        print(exhale_hold)
        if exhale_hold is None:
            return apology("Exhale Hold must be an integer 0 or greater.", 400)

        rounds = validate_field("rounds")
        if rounds is None or rounds == 0:
            return apology("Rounds must be an integer number greater than 0. At least breathe for 1 round!", 403)

        db.execute("UPDATE breathworks SET name=?, description=?, inhale=?, inhale_hold=?, exhale=?, exhale_hold=?, rounds=? WHERE user_id=? AND id=?",
                   name, description, inhale, inhale_hold, exhale, exhale_hold, rounds, session["user_id"], breathwork_id)
        return redirect("/editor")


@app.route("/practice", methods=["GET", "POST"])
@login_required
def practice():
    if request.method == "GET":
        breathwork = db.execute(
            "SELECT * FROM breathworks WHERE id = ?", request.args.get("breathworkId"))
        return render_template("practice.html", breathwork=breathwork[0])

    if request.method == "POST":
        # insert the data in logs
        # get the value of these duration id
        breathwork_id = request.form.get("id")
        breathwork_duration = int(round(float(request.form.get("duration"))))
        breathwork_notes = request.form.get("notes")

        # Log data to history table
        print("Values:", breathwork_id, breathwork_duration, breathwork_notes)
        try:
            db.execute("INSERT INTO logs (user_id,breathwork_id,duration_seconds,notes) Values(?,?,?,?)",
                       session["user_id"], breathwork_id, breathwork_duration, breathwork_notes)
        except Exception as e:
            print("Error:", e)

        return redirect("/")
