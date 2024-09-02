import requests

def get_bybit_token_price(symbol, check):
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {
        'category': 'spot',
        'symbol': symbol
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['retMsg'] == 'Not supported symbols':
        return

    if check in ['to_check']:
        for token in data['result']['list']:
            token_dir = {'symbol': token['symbol'], 'price': token['lastPrice']}
            return token_dir
    else:
        token_dir = []
        for token in data['result']['list']:
            token_dir.append({'symbol': token['symbol'], 'price': token['lastPrice']})
        return token_dir

def get_gateio_token_price(symbol, check):
    url = f'https://api.gateio.ws/api/v4/spot/tickers'
    params = {
        'currency_pair': f'{symbol}_USDT' if symbol is not None else None
    }
    response = requests.get(url, params=params)
    data = response.json()

    token_dir = []
    for token in data:
        token_dir.append({'symbol': token['currency_pair'], 'price': token['last']})
    for token in token_dir:
        temp = token['symbol'].split('_')
        token['symbol'] = f'{temp[0]}{temp[1]}'
    return token_dir

def get_mexc_token_price(symbol, check):
    url_to_check = 'https://api.mexc.com/api/v3/ticker/24hr'
    url_check = 'https://api.mexc.com/api/v3/defaultSymbols'
    params = {
        'symbol': symbol
    }
    response = requests.get(url_to_check, params=params)
    data = response.json()

    try:
        if check in ['to_check']:
            token_dir = {'symbol': data['symbol'], 'price': data['lastPrice']}
            return token_dir
    except KeyError:
        return None

def exchanges_checker(symbol, price1, price2):
    k = price1 / price2
    if 0.7 <= k <= 0.97 or 1.30 >= k >= 1.03:
        return symbol, price1, price2


def get_spread_start():

    '''dir = get_gateio_token_price(None, 'checker')
    for i in dir:
        token = get_bybit_token_price(i['symbol'], 'to_check')
        if token:
            result = exchanges_checker(token['symbol'], float(i['price']), float(token['price']))
            if result:
                symbol, price_1, price_2 = result
                return symbol, price_1, price_2'''

    dir = get_gateio_token_price(None, 'checker')
    for i in dir:
        token = get_mexc_token_price(i['symbol'], 'to_check')
        if token:
            result = exchanges_checker(token['symbol'], float(i['price']), float(token['price']))
            if result:
                symbol, price_1, price_2 = result
                return symbol, price_1, price_2

    return None, None, None