from flask import render_template, session, request, redirect
import cs50
import currencies
from error import apology

db = cs50.SQL("sqlite:///portfolio.db")

def add_coin_to_portfolio():
    if request.method == "POST":
        pid = request.form.get("pid")
        db.execute("INSERT INTO portfolio_currency (portfolio_id, cryptocurrency_id, quantity, price) VALUES (?, ?, ?, ?)",
                    pid, request.form.get("cid"), request.form.get("amount"), request.form.get("price"))
        return redirect(f"/portfolio?pid={pid}")
    else:
        pid = request.args.get("pid")
        currency_id = request.args.get("cid")
        print(f"c: {currency_id}")
        if currency_id == None:
            # get coins from the database
            coin_list = currencies.get_coinlist_from_db()
            print(f"c: {coin_list}")
            return render_template("currencies.html", coins=coin_list, pid=pid, add_coin=True)
        else:
            return render_template("add_currency.html", pid=pid, cid=currency_id)


def get_users_portfolios(userid:int):
    return db.execute("SELECT * FROM portfolios WHERE user_id = ?", userid)


def delete():
    portfolio_id = request.args.get("id")
    db.execute("DELETE FROM portfolios WHERE id = ?", portfolio_id)
    print(portfolio_id)
    return redirect("/portfolio")


def create():
    """
        
    """
    if request.method == "POST":
        portfolio_id = db.execute("INSERT INTO portfolios (user_id, name) VALUES (?, ?)", session["user_id"], request.form.get("name"))
        return redirect(f"/portfolio?pid={portfolio_id}")
    
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


def portfolio():
    """
        
    """
    currencies.update_coin_values_and_return()
    coinlist = []
    exists = False
    if session["user_id"] == None:
        return apology("You're not logged in.", 400)
    portfolio_id = request.args.get("pid")
    portfolios = get_users_portfolios(session["user_id"])
    if portfolio_id == None:
        if portfolios == None:
            return redirect(f"/create_portfolio")
        portfolio_id = portfolios[0]["id"]
    coins = db.execute("SELECT * FROM portfolio_currency INNER JOIN currencies ON " \
                       " cryptocurrency_id = currencies.id WHERE portfolio_id = ? ", portfolio_id)
    for coin in coins:
        for cl_coin in coinlist:
            if cl_coin.id == coin["id"]:
                cl_coin.price = (cl_coin.price + coin["price"]) / 2
                cl_coin.quantity += coin["quantity"]
                exists = True

        if exists != True:                
            ccoin = crypto_coin(id=coin["id"], icon_url=coin["icon_url"], symbol=coin["symbol"], name=coin["name"], quantity=coin["quantity"], price=coin["price"], current_price=coin["current_price"])
            coinlist.append(ccoin)
        exists = False


    # else:
    #     for portfolio in portfolios:
    #         if portfolio["id"] == portfolio_id:   
    #             coins = db.execute("SELECT * FROM currencies WHERE id = ?", portfolio[""])
    return render_template("portfolio.html", portfolios=portfolios, coins=coinlist, pid=portfolio_id)

# CREATE TABLE portfolios (
# id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# user_id INTEGER,
# name TEXT,
# FOREIGN KEY (user_id) REFERENCES users(id)
# );

# CREATE TABLE portfolio_currency (
# id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# portfolio_id INTEGER NOT NULL,
# cryptocurrency_id INTEGER NOT NULL,
# quantity REAL NOT NULL,
# price REAL NOT NULL,
# );