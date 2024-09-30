from flask import render_template, request, redirect, session

from error import apology
import bybit, cgecko

import cs50

db = cs50.SQL("sqlite:///portfolio.db")

def update_currency_db() -> None:
    """updates our database with coin data"""
    coin_list = cgecko.get_coin_list()
    for coin in coin_list:
        # check if the coin is in our database
        rows = db.execute("SELECT * FROM currencies WHERE cgid = ?", coin['id'])
        if rows is None or len(rows) < 1:
            # if it isn't we add it
            # TODO: errorcheck
            print(f"inserting coin: {coin}")
            db.execute("INSERT INTO currencies (cgid, symbol, name) VALUES (?, ?, ?)", coin['id'], coin['symbol'], coin['name'])
        # otherwise we check if the data matches
        elif len(rows) == 1:
            if rows[0]['symbol'] != coin['symbol'] or rows[0]['name'] != coin['name']:
                # gotta throw an error here
                return apology(f"for coin with id: {coin['cgid']} there is a missmatch of data", 500)
        continue


def overview():
    #s_time_in_seconds = bybit.get_server_time_in_seconds()
    #bybit.get_kline("spot", "BTCUSDT", 60)
    #tickers = bybit.get_tickers("spot")
    coin_list = cgecko.get_coin_list_w_market_data()
    for coin in coin_list:
        print(f"coin: {coin}")
        #print(f"id: {coin['id']} - symbol: {coin['symbol']} - name: {coin['name']} - platform: {coin['platforms']}")
    return render_template("currencies.html", coins=coin_list)