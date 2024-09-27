from pybit.unified_trading import HTTP
import error

session = HTTP(testnet=True)

def get_server_time() -> dict:
    return session.get_server_time()

def get_server_time_in_seconds() -> str:
    return session.get_server_time()['result']['timeSecond']


def get_kline(category, symbol, interval = 60, start = None, end = None, limit = 200):
    print( session.get_kline(category=category, symbol=symbol, interval=interval, start=start, end=end, limit=limit) )

def get_all_tickers(category):
    try:
        resp = session.get_tickers(category=category)
        if resp["retMsg"] != "OK":
            return error.apology("yikes")

        resp = resp["result"]["list"]
        symbols = []
        for elem in resp:
            symbols.append(elem["symbol"])
        return symbols

    except:
        return error.apology("yikes")


def get_tickers(category, symbol = None, baseCoin = None, expDate = None):
    try:
        resp = session.get_tickers(category=category, symbol=symbol, baseCoin=baseCoin, expDate=expDate)
        if resp["retMsg"] != "OK":
            return error.apology("yikes")

        ret = []
        for elem in resp["result"]["list"]:
            if elem["volume24h"] != '0':
                print(elem)
                ret.append(elem)
        return ret
        #return resp["result"]["list"]

    except:
        return error.apology("yikes")
