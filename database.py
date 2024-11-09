import cs50
from os.path import exists

import database_schema

db = None
file_name = "portfolio.db"
file_created = False
table_names = ["users", "currencies", "portfolios", "portfolio_currency"]

def sql_file_exists(filename) -> bool:
    if not exists(f"./{filename}"):
        print(f"file not found. {file_name} creating ...", end=" ")
        open(filename, "w")
        global file_created
        file_created = True

    return exists(f"./{filename}")


def sql_table_exists(table: str) -> bool:
    return db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name = ?", table)


def sql_table_check(tablenames: list[int]) -> None:
    for item in tablenames:
        if not sql_table_exists(item):
            print(f"table not found. {item} creating ...", end=" ")
            if item == "users":
                db.execute(database_schema.sql_table_users_query)
            if item == "currencies":
                db.execute(database_schema.sql_table_currencies_query)
            if item == "portfolios":
                db.execute(database_schema.sql_table_portfolios_query)
            if item == "portfolio_currency":
                db.execute(database_schema.sql_table_portfolio_currency_query)
            print("done")

    
if not sql_file_exists(file_name):
    print(f"error creating database ... exiting.")
else:
    db = cs50.SQL(f"sqlite:///{file_name}")
    sql_table_check(table_names)