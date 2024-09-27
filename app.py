import os
from flask import Flask, render_template, request, redirect, session
from flask_session import Session

import users, error, bybit

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_COOKIE_NAME"] = "cportfolio"
app.session_cookie_name = "cportfolio"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return users.register()

@app.route("/login", methods=["GET", "POST"])
def login():
    return users.login()
    
@app.route("/logout")
def logout():
    return users.logout()

@app.route("/crypto")
def crypto():
    s_time_in_seconds = bybit.get_server_time_in_seconds()
    #bybit.get_kline("spot", "BTCUSDT", 60)
    tickers = bybit.get_tickers("linear")
    return render_template("cryptos.html", tickers=tickers)

@app.route("/portfolio")
def portfolio():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

