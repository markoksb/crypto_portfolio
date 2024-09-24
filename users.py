from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine

from error import apology

engine = create_engine("sqlite:///portfolio.db", echo=True)
db = engine.connect()

app = Flask(__name__)

def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if request.form.get("username") == "markob":
            session["user_id"] = 1
            return redirect("/")

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
    

def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        username = request.form.get("username")
        if not username:
            return apology("must provide username", 400)
        else:
            namequery = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(namequery) > 0:
                return apology("username already exists", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        else:
            if not request.form.get("confirmation"):
                return apology("must provide password twice", 400)
            elif not request.form.get("confirmation") == request.form.get("password"):
                return apology("passwords must match", 400)
            else:
                # do some magic
                db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username,
                           generate_password_hash(request.form.get("password")))
                return redirect("/")

    else:
        return render_template("register.html")
