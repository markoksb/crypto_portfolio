import requests

from error import apology
from key import coingecko_api_key

url = "https://api.coingecko.com/api/v3/"
headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": f"{coingecko_api_key}"
}
def request(endpoint:str):
    try:
        response = requests.get(url+endpoint, headers=headers)
    except:
        return apology("error with api request")
    if response.status_code != 200:
        return apology(response.reason, response.status_code)
    response.close()
    return response

def test():
    endpoint = "coins/list"
    return request(endpoint=endpoint).json()


def get_coin_list():
    endpoint = "coins/list"
    return request(endpoint=endpoint).json()


def get_coin_list_w_market_data():
    endpoint = "coins/markets?vs_currency=usd"
    return request(endpoint=endpoint).json()
