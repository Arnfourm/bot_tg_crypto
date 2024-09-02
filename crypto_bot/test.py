import requests

def get_bybit_token_price(symbol):
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {
        'category': 'spot',
        'symbol': f'{symbol}' if symbol is not None else None
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data['retMsg'] == 'Not supported symbols':
        return

    token_dir = []
    for token in data['result']['list']:
        token_dir.append({'symbol': token['symbol'], 'price': token['lastPrice']})
    return token_dir

def get_gateio_token_price(symbol):
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

def exchanges_checker(symbol, price1, price2):
    k = price1 / price2
    if k <= 0.95 or k >= 1.05:
        print(symbol, price1, price2)
    else:
        return

def checker_start():
    dir = get_gateio_token_price(None)
    for i in dir:
        token = get_bybit_token_price(i['symbol'])
        if token is not None:
            for crypto in token:
                exchanges_checker(crypto['symbol'], float(i['price']), float(crypto['price']))

    '''dir = get_bybit_token_price(None)
    for i in dir:
        print(i['symbol'], i['price'])'''



checker_start()




'''htx - websocket market data'''