from flask import render_template
from datetime import datetime, timedelta
from error import apology
import cgecko
from database import db

def get_coinlist_from_db():
    """get all the currencies"""
    return db.execute("SELECT * FROM currencies ORDER BY market_cap DESC")


def get_coin_from_db_by_id(coin_id:int):
    """returns a currency based on our coin id"""
    return db.execute("SELECT * FROM currencies WHERE id = ?", coin_id)


def get_coin_from_db(coin_cgid:str):
    """returns a currency based on coingecko id"""
    return db.execute("SELECT * FROM currencies WHERE cgid = ?", coin_cgid)


def update_coin_in_db(coin_id_csv) -> None:
    """update all the coins by coingecko id"""
    coins = cgecko.get_coin_update(coin_id_csv)
    for coin in coins:
        db.execute("UPDATE currencies SET current_price = ?, market_cap = ?, high_24h = ?, low_24h = ?, ath = ?, ath_date = ?, atl = ?, atl_date = ?, cg_update_date = ?, price_change_percent_1h = ?, price_change_percent_24h = ?, price_change_percent_7d = ?, price_change_percent_30d = ?, update_date = ? WHERE cgid = ?",
            coin['current_price'], coin['market_cap'], coin['high_24h'], coin['low_24h'], coin['ath'],
            coin['ath_date'], coin['atl'], coin['atl_date'], coin['last_updated'], coin['price_change_percentage_1h_in_currency'],
            coin['price_change_percentage_24h_in_currency'], coin['price_change_percentage_7d_in_currency'], coin['price_change_percentage_30d_in_currency'], datetime.now(), coin['id']
        )


def update_currency_db() -> None:
    """updates our database with coin data"""
    coin_list = cgecko.get_coin_list_w_market_data()
    for coin in coin_list:
        # check if the coin is in our database
        rows = get_coin_from_db(coin['id'])
        if rows is not None and len(rows) >= 1:
            if rows[0]['symbol'] != coin['symbol'] or rows[0]['name'] != coin['name']:
                # gotta throw an error here
                return apology(f"for coin with id: {coin['cgid']} there is a missmatch of data", 500)            
        # if it isn't we add it
        db.execute("INSERT INTO currencies (cgid, symbol, name, icon_url, current_price, market_cap, high_24h, low_24h, ath, ath_date, atl, atl_date, cg_update_date, price_change_percent_1h, price_change_percent_24h, price_change_percent_7d, price_change_percent_30d, update_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            coin['id'], coin['symbol'], coin['name'], coin['image'], coin['current_price'],
            coin['market_cap'], coin['high_24h'], coin['low_24h'], coin['ath'], coin['ath_date'],
            coin['atl'], coin['atl_date'], coin['last_updated'], coin['price_change_percentage_1h_in_currency'], coin['price_change_percentage_24h_in_currency'],
            coin['price_change_percentage_7d_in_currency'], coin['price_change_percentage_30d_in_currency'], datetime.now()
        )


def update_coin_values() -> None:
    """
        Read data from DB.\n
        Should the data be outdated, update the DB.\n
    """
    # get coins from the database
    coin_list = get_coinlist_from_db()
    
    coins_to_update = ""
    # check if our coin data is somewhat recent for each coin
    for coin in coin_list:
        # if not, add the coin to a csv list
        if datetime.strptime(coin['update_date'], "%Y-%m-%d %H:%M:%S") < datetime.now() - timedelta(minutes=5):
            coins_to_update += f"{coin['cgid']},"
    # if list is not empty do an update
    if coins_to_update != "":
        #print("updating coin data ...", end="")
        update_coin_in_db(coins_to_update)


def overview():
    """
        Main function for the currencies view.\n
    """
    update_coin_values()
    coin_list = get_coinlist_from_db()
    # TODO: this is kinda nonsense but we need it if the DB is empty/reset or w/e
    # idea is to have a function for this that also gets more than the top100 coins (#pagination)
    if len(coin_list) < 50:
        update_currency_db()

    return render_template("currencies.html", coins=coin_list)