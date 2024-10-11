from flask import render_template, session, request, redirect
import cs50

db = cs50.SQL("sqlite:///portfolio.db")

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
        return redirect(f"/portfolio?id={portfolio_id}")
    
    return render_template("portfolio_new.html")


def portfolio():
    """
        
    """
    portfolios = get_users_portfolios(session["user_id"])
    currencies = ""
    return render_template("portfolio.html", portfolios=portfolios, currencies=currencies)

# CREATE TABLE portfolios (
# id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
# user_id INTEGER,
# name TEXT,
# FOREIGN KEY (user_id) REFERENCES Users(id)
# );

# CREATE TABLE portfolio_currency (
# portfolio_id INTEGER NOT NULL,
# cryptocurrency_id INTEGER NOT NULL,
# quantity REAL NOT NULL,
# price REAL NOT NULL,
# PRIMARY KEY (portfolio_id, cryptocurrency_id),
# FOREIGN KEY (portfolio_id) REFERENCES Portfolios(id),
# FOREIGN KEY (cryptocurrency_id) REFERENCES Cryptocurrencies(id)
# );