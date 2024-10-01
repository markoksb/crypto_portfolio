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
    vs_currency = "usd"
    page_size = "100"
    page = "1"
    price_change_percentage = "1h,24h,7d,30d"
    endpoint = f"coins/markets?vs_currency={vs_currency}&page_size={page_size}&page={page}&price_change_percentage={price_change_percentage}"
    return request(endpoint=endpoint).json()
# return value
# {
#     "id": "bitcoin",
#     "symbol": "btc",
#     "name": "Bitcoin",
#     "image": "https://coin-images.coingecko.com/coins/images/1/large/bitcoin.png?1696501400",
#     "current_price": 62648,
#     "market_cap": 1237899902658,
#     "market_cap_rank": 1,
#     "fully_diluted_valuation": 1315489143696,
#     "total_volume": 34184618434,
#     "high_24h": 64131,
#     "low_24h": 62658,
#     "price_change_24h": -1338.8275872219601,
#     "price_change_percentage_24h": -2.09234,
#     "market_cap_change_24h": -27152186622.506104,
#     "market_cap_change_percentage_24h": -2.14633,
#     "circulating_supply": 19761393,
#     "total_supply": 21000000,
#     "max_supply": 21000000,
#     "ath": 73738,
#     "ath_change_percentage": -14.8941,
#     "ath_date": "2024-03-14T07:10:36.635Z",
#     "atl": 67.81,
#     "atl_change_percentage": 92447.20623,
#     "atl_date": "2013-07-06T00:00:00.000Z",
#     "roi": null,
#     "last_updated": "2024-10-01T13:55:06.346Z",
#     "price_change_percentage_1h_in_currency": -1.597395697490496,
#     "price_change_percentage_24h_in_currency": -2.092341671162888,
#     "price_change_percentage_7d_in_currency": -1.2535379112507992
# }