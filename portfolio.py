from flask import render_template, session, request, redirect
import currencies, req_login
from error import apology
from database import db

class crypto_coin(object):
    def __init__(self, id, icon_url, symbol, name, quantity, price, current_price):
        self.id = id
        self.icon_url = icon_url
        self.symbol = symbol
        self.name = name
        self.quantity = quantity
        self.price = price
        self.current_price = current_price

    def __str__(self):
        return (f"Crypto Coin [ID: {self.id}, Symbol: {self.symbol}, Name: {self.name}, "
                f"Quantity: {self.quantity}, Purchase Price: ${self.price:.2f}, "
                f"Current Price: ${self.current_price:.2f}]")


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


def validate_float_positive(value, name: str):
    """Validate value to be a positive number"""
    try:
        val = float(value)
        if val < 0:
            raise ValueError(f"{name} must be positive.")
        return val
    except ValueError as e:
        return str(e)
    except Exception as e:
        return str(e)
    

def validate_int_positive(value, name: str):
    """Validate value to be a positive integer"""
    try:
        val = int(value)
        if val < 0:
            raise ValueError(f"{name} must be positive.")
        return val
    except ValueError as e:
        return str(e)
    except Exception as e:
        return str(e)


def validate_id_in_table(table_name: str, id_value: int, id_name: str = "id") -> bool:
    """Check if an ID exists in the specified table."""
    return db.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {id_name} == ?", id_value)[0]["COUNT(*)"] == 1


def get_total_quantity(portfolio_id: int, coin_id: int) -> float:
        """Summerize the quantity of a specific coin in a portfolio."""
        res = db.execute("SELECT quantity FROM portfolio_currency WHERE portfolio_id == ? AND cryptocurrency_id == ?",
                    portfolio_id, coin_id)
        return sum(row["quantity"] for row in res)


def get_portfolio_entries(portfolio_id: int) -> list:
    """gets all the purchase entries for the given portfolio"""
    coin_list = None
    try:
        coin_list = db.execute("SELECT *, portfolio_currency.id AS id, currencies.id AS cid FROM portfolio_currency INNER JOIN currencies ON " \
                        " portfolio_currency.cryptocurrency_id = cid WHERE portfolio_id = ? ", portfolio_id)
    except:
        return apology("error getting portfolio data from the database.", 500)
    return coin_list


def generate_coin_list_for_portfolio(portfolio_id: int, coin_list: list = None) -> list:
    """generates a list of coins from the database entries made to the given portfolio"""
    if coin_list == None:
        coin_list = []
    list_of_entries = get_portfolio_entries(portfolio_id)
    for entry in list_of_entries:
        exists = False
        for coin in coin_list:
            if coin.id == entry["cid"]:
                if entry["quantity"] < 0:
                    combined_quantity = coin.quantity + entry["quantity"]
                else:
                    combined_quantity = coin.quantity + entry["quantity"]
                    coin.price = (coin.price * coin.quantity + entry["price"] * entry["quantity"]) / combined_quantity
                coin.quantity = combined_quantity
                exists = True

        if exists == False:
            ccoin = crypto_coin(id=entry["cid"], icon_url=entry["icon_url"], symbol=entry["symbol"], name=entry["name"], quantity=entry["quantity"], price=entry["price"], current_price=entry["current_price"])
            coin_list.append(ccoin)
    return coin_list


def generate_coin_list_for_overview(portfolio_list: list) -> list:
    coin_list = []
    for portfolio in portfolio_list:
        generate_coin_list_for_portfolio(portfolio["id"], coin_list)
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
    return (coin.current_price - coin.price) * coin.quantity


def calculate_pnl(coin_list: list[crypto_coin]) -> float:
    total = 0
    for coin in coin_list: 
        total += calculate_pnl_per_coin(coin)
    return total


@req_login.login_required
def rem_transaction():
    portfolio_id = validate_int_positive(request.args.get("folioid"), "PortfolioID")
    if isinstance(portfolio_id, str):
        return apology(f"Error: {portfolio_id}")
    if not validate_id_in_table("portfolios", portfolio_id):
        return apology("Error finding entry\nplease try again.")
    
    entry_id = validate_int_positive(request.args.get("entryid"), "EntryID")
    if isinstance(entry_id, str):
        return apology(f"Error: {entry_id}")
    if not validate_id_in_table("portfolio_currency", entry_id):
        return apology("Error finding entry\nplease try again.")
    
    db.execute("DELETE FROM portfolio_currency WHERE id = ?", entry_id)
    return redirect(f"/portfolio?folioid={portfolio_id}&tr=1")


@req_login.login_required
def add_coin_to_portfolio():
    """add an entry for a purchase"""
    if request.method == "POST":
        portfolio_id = validate_int_positive(request.form.get("folioid"), "PortfolioID")
        if isinstance(portfolio_id, str):
            return apology(f"Error: {portfolio_id}")
        if not validate_id_in_table("portfolios", portfolio_id):
            return apology("Error finding the portfolio\nplease try again.")
        
        coin_id = validate_int_positive(request.form.get("cid"), "CoinID")
        if isinstance(coin_id, str):
            return apology(f"Error: {coin_id}")
        if not validate_id_in_table("currencies", coin_id):
            return apology("Error finding that coin\nplease try again.")
        
        amount = validate_float_positive(request.form.get("amount"), "Amount")
        if isinstance(amount, str):
            return apology(f"Error: {amount}")
        
        price = validate_float_positive(request.form.get("price"), "Price")
        if isinstance(price, str):
            return apology(f"Error: {price}")
        
        db.execute("INSERT INTO portfolio_currency (portfolio_id, cryptocurrency_id, quantity, price) VALUES (?, ?, ?, ?)",
                    portfolio_id, coin_id, amount, price)
        return redirect(f"/portfolio?folioid={portfolio_id}")
    else:
        portfolio_id = validate_int_positive(request.args.get("folioid"), "PortfolioID")
        if isinstance(portfolio_id, str):
            return apology(f"Error: {portfolio_id}")
        if not validate_id_in_table("portfolios", portfolio_id):
            return apology("Error finding the portfolio\nplease try again.")
        
        currency_id = request.args.get("cid")
        if currency_id == None:
            # get coins from the database
            coin_list = currencies.get_coinlist_from_db()
            return render_template("currencies.html", coins=coin_list, portfolio_id=portfolio_id, add_coin=True)

        return render_template("portfolio_transaction.html", portfolio_id=portfolio_id, coin=currencies.get_coin_from_db_by_id(currency_id)[0], request=request)
    

def rem_coin_from_portfolio():
    """add an entry for a sell"""
    if request.method == "POST":
        portfolio_id = validate_int_positive(request.form.get("folioid"), "PortfolioID")
        if isinstance(portfolio_id, str):
            return apology(f"Error: {portfolio_id}")
        if not validate_id_in_table("portfolios", portfolio_id):
            return apology("Error finding the portfolio\nplease try again.")
        
        coin_id = validate_int_positive(request.form.get("cid"), "CoinID")
        if isinstance(coin_id, str):
            return apology(f"Error: {coin_id}")
        if not validate_id_in_table("currencies", coin_id):
            return apology("Error finding that coin\nplease try again.")
        
        amount = validate_float_positive(request.form.get("amount"), "Amount")
        if isinstance(amount, str):
            return apology(f"Error: {amount}")
        
        total = validate_float_positive(request.form.get("total"), "Total")
        if isinstance(total, str):
            return apology(f"Error: {total}")
        
        price = total / amount
        amount *= -1
        db.execute("INSERT INTO portfolio_currency (portfolio_id, cryptocurrency_id, quantity, price) VALUES (?, ?, ?, ?)",
                    portfolio_id, coin_id, amount, price)
        return redirect(f"/portfolio?folioid={portfolio_id}")
    
    else:
        portfolio_id = validate_int_positive(request.args.get("folioid"), "PortfolioID")
        if isinstance(portfolio_id, str):
            return apology(f"Error: {portfolio_id}")
        if not validate_id_in_table("portfolios", portfolio_id):
            return apology("Error finding the portfolio\nplease try again.")
        
        coin_id = validate_int_positive(request.args.get("cid"), "PortfolioID")
        if isinstance(coin_id, str):
            return apology(f"Error: {coin_id}")
        if not validate_id_in_table("currencies", coin_id):
            return apology("Error finding the portfolio\nplease try again.")

        quantity = get_total_quantity(portfolio_id, coin_id)
        return render_template("portfolio_transaction.html", portfolio_id=portfolio_id, coin=currencies.get_coin_from_db_by_id(coin_id)[0], request=request, amount_max=quantity)


@req_login.login_required
def portfolio():
    """
        accumulates data based on the users portfolio and renders the template.
    """
    currencies.update_coin_values()
    if session["user_id"] == None:
        return apology("You're not logged in.", 400)
    
    portfolios = get_users_portfolios(session["user_id"])
    if not portfolios:
        return redirect(f"/create_portfolio")
    
    if request.args.get("folioid") == None:
        portfolio_id = -1
    else:
        try:
            portfolio_id = int(request.args.get("folioid"))
        except Exception as e:
            return apology("Error. Please send help.", 500)
        
    if request.args.get("tr") == "1":
        if portfolio_id > 0:
            entries = get_portfolio_entries(portfolio_id)
            return render_template("transactions.html", entries=entries, portfolio_id=portfolio_id)
        entries = []
        for portfolio in portfolios:
            entries += get_portfolio_entries(portfolio["id"])
        return render_template("transactions.html", entries=entries, portfolio_id=portfolio_id)

    if portfolio_id == -1:
        coinlist = generate_coin_list_for_overview(portfolios)
    else:
        coinlist = generate_coin_list_for_portfolio(portfolio_id)

    coinlist.sort(key=lambda coin: calculate_pnl_per_coin(coin), reverse=True)

    return render_template("portfolio.html",  portfolio_id=portfolio_id, portfolios=portfolios, coins=coinlist, value=calculate_total_value(coinlist), change=calculate_change(coinlist), pnl=calculate_pnl(coinlist), coinchange=calculate_change_per_coin)
