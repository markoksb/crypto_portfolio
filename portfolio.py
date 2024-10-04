from flask import render_template, session

def portfolio():
    """
        Main function for the currencies view.\n
        Read data from DB.\n
        Should the data not exist or is outdated, update the DB.\n
        Render the html with the coin data.
    """
    return render_template("portfolio.html")