from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash

from error import apology
import bybit

def overview():
    s_time_in_seconds = bybit.get_server_time_in_seconds()
    #bybit.get_kline("spot", "BTCUSDT", 60)
    tickers = bybit.get_tickers("spot")
    return render_template("currencies.html", tickers=tickers)