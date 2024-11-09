sql_table_currencies_query = """
CREATE TABLE currencies (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
cgid TEXT UNIQUE NOT NULL,
symbol TEXT NOT NULL,
name TEXT NOT NULL,
icon_url TEXT NOT NULL,
current_price REAL NOT NULL,
market_cap INTEGER NOT NULL,
high_24h REAL NOT NULL,
low_24h REAL NOT NULL,
ath REAL NOT NULL,
ath_date TEXT NOT NULL,
atl REAL NOT NULL,
atl_date TEXT NOT NULL,
cg_update_date TEXT NOT NULL,
price_change_percent_1h REAL,
price_change_percent_24h REAL NOT NULL,
price_change_percent_7d REAL,
price_change_percent_30d REAL,
update_date TEXT NOT NULL
);
"""

sql_table_users_query = """
CREATE TABLE users (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
username TEXT NOT NULL,
password_hash TEXT NOT NULL
);
"""

sql_table_portfolios_query = """
CREATE TABLE portfolios (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
user_id INTEGER,
name TEXT,
FOREIGN KEY (user_id) REFERENCES Users(id)
);
"""

sql_table_portfolio_currency_query = """
CREATE TABLE portfolio_currency (
id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
portfolio_id INTEGER NOT NULL,
cryptocurrency_id INTEGER NOT NULL,
quantity REAL NOT NULL,
price REAL NOT NULL
);
"""