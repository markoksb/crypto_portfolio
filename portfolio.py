from flask import render_template, session, request, redirect
import currencies, req_login
from error import apology
from database import db

@req_login.login_required
def add_coin_to_portfolio():
    """add an entry for a purchase"""
    if request.method == "POST":
        portfolio_id = request.form.get("folioid")
        db.execute("INSERT INTO portfolio_currency (portfolio_id, cryptocurrency_id, quantity, price) VALUES (?, ?, ?, ?)",
                    portfolio_id, request.form.get("cid"), request.form.get("amount"), request.form.get("price"))
        return redirect(f"/portfolio?folioid={portfolio_id}")
    else:
        portfolio_id = request.args.get("folioid")
        currency_id = request.args.get("cid")
        if currency_id == None:
            # get coins from the database
            coin_list = currencies.get_coinlist_from_db()
            return render_template("currencies.html", coins=coin_list, portfolio_id=portfolio_id, add_coin=True)

        return render_template("add_currency.html", portfolio_id=portfolio_id, coin=currencies.get_coin_from_db_by_id(currency_id)[0])


@req_login.login_required
def get_users_portfolios(userid:int):
    """get a list of portfolios for the user"""
    return db.execute("SELECT * FROM portfolios WHERE user_id = ?", userid)


@req_login.login_required
def delete():
    """deletes a portfolio"""
    if request.method == "POST":
        portfolio_id = request.form.get("folioid")
        db.execute("DELETE FROM portfolios WHERE id = ?", portfolio_id)
        db.execute("DELETE FROM portfolio_currency WHERE portfolio_id = ?", portfolio_id)
        return redirect("/portfolio")
    
    portfolio_id=request.args.get("folioid")
    portfolio = db.execute("SELECT * FROM portfolios WHERE id = ? ", portfolio_id)
    return render_template("portfolio_del.html", portfolio=portfolio[0])


@req_login.login_required
def create():
    """
        creates a new portfolio
    """
    if request.method == "POST":
        portfolio_id = db.execute("INSERT INTO portfolios (user_id, name) VALUES (?, ?)", session["user_id"], request.form.get("name"))
        return redirect(f"/portfolio?folioid={portfolio_id}")
    
    return render_template("portfolio_new.html")

class crypto_coin(object):
    def __init__(self, id, icon_url, symbol, name, quantity, price, current_price):
        self.id = id
        self.icon_url = icon_url
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        self.price = price
        self.current_price = current_price


def get_portfolio_entries(portfolio_id: int) -> list:
    """gets all the purchase entries for the given portfolio"""
    coin_list = None
    try:
        coin_list = db.execute("SELECT * FROM portfolio_currency INNER JOIN currencies ON " \
                        " cryptocurrency_id = currencies.id WHERE portfolio_id = ? ", portfolio_id)
    except:
        return apology("error getting portfoliodata from the database.", 500)
    return coin_list


def generate_coin_list_for_portfolio(portfolio_id: int) -> list:
    """generates a list of coins from the database entries made to the given portfolio"""
    coin_list = []
    list_of_purchases = get_portfolio_entries(portfolio_id)
    for entry in list_of_purchases:
        exists = False
        for coin in coin_list:
            if coin.id == entry["id"]:
                coin.price = (coin.price + entry["price"]) / 2
                coin.quantity += entry["quantity"]
                exists = True

        if exists == False:
            ccoin = crypto_coin(id=entry["id"], icon_url=entry["icon_url"], symbol=entry["symbol"], name=entry["name"], quantity=entry["quantity"], price=entry["price"], current_price=entry["current_price"])
            coin_list.append(ccoin)
    return coin_list


def calculate_total_value(coin_list: list[crypto_coin]) -> float:
    total = 0
    for coin in coin_list:
        total += coin.current_price * coin.quantity
    return total


def calculate_change_per_coin(coin: crypto_coin, time: str = "24h") -> float:
    if time == "24h":
        coin_change = currencies.get_coin_from_db_by_id(coin.id)[0]["price_change_percent_24h"]
    return ( coin_change / 100 ) * coin.current_price


def calculate_change(coin_list: list[crypto_coin], time: str = "24h") -> float:
    total = 0
    for coin in coin_list: 
        total += calculate_change_per_coin(coin, time) * coin.quantity
    return total


def calculate_pnl_per_coin(coin: crypto_coin) -> float:
    return coin.current_price - coin.price


def calculate_pnl(coin_list: list[crypto_coin]) -> float:
    total = 0
    for coin in coin_list: 
        total += calculate_pnl_per_coin(coin) * coin.quantity
    return total


@req_login.login_required
def portfolio():
    """
        accumulates data based on the users portfolio and renders the template.
    """
    currencies.update_coin_values_and_return()
    coinlist = []
    if session["user_id"] == None:
        return apology("You're not logged in.", 400)
    
    portfolios = get_users_portfolios(session["user_id"])
    if not portfolios:
        return redirect(f"/create_portfolio")
    
    portfolio_id = request.args.get("folioid")
    if portfolio_id == None:
        portfolio_id = portfolios[0]["id"]

    coinlist = generate_coin_list_for_portfolio(portfolio_id)

    return render_template("portfolio.html",  portfolio_id=portfolio_id, portfolios=portfolios, coins=coinlist, value=calculate_total_value(coinlist), change=calculate_change(coinlist), pnl=calculate_pnl(coinlist))
