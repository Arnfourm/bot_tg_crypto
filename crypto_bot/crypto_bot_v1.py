import telebot
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from spread import get_spread_start

def crypto_cmc_price_get(symbol, quantity):
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
    params = {
        'amount': quantity,
        'convert': 'USD',
        'symbol': symbol
    }
    headers = {
        'X-CMC_PRO_API_KEY': '84be6ecd-6c03-4a4f-82f1-c8782d7d8895'
    }
    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)

        price = data['data']['quote']['USD']['price']

        if price > 1000:
            return round(price)
        elif 1000 > price > 1:
            return round(price, 2)
        elif 1 > price > 0.01:
            return round(price, 3)
        else:
            return f'{price:.8f}'

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print('Ошибка: ', e)

def bot():
    bot = telebot.TeleBot('7542287362:AAFj9E4xeiW5Seod0vUhAX17Vlq3erRFRv8')

    @bot.message_handler(commands = ['start'])
    def start(message):
        bot.send_message(message.chat.id, 'В боте можно узнать информацию по криптоактивам \nЧтобы узнать больше '
                                          'нажмите /help')

    @bot.message_handler(commands = ['help'])
    def help(message):
        bot.send_message(message.chat.id, '/start - Начать работу бота \n/help - Все команды \n/cmc - Узнать '
                                          'информацию о токене по CoinMarketCap.')

    @bot.message_handler(commands= ['cmc'])
    def cmc(message):
        text = message.text.split(' ')

        quantity, symbol = (int(text[1]), text[2].upper()) if len(text) == 3 else (1, text[1].upper())

        price = crypto_cmc_price_get(symbol, quantity)
        bot.send_message(message.chat.id, f'Цена {quantity} {symbol} - {price} usdt')

    @bot.message_handler(commands=['spread'])
    def get_spread_bot(message):
        bot.send_message(message.chat.id, 'Поиск начался, примерно время 5-10 минут')
        symbol, price_1, price_2 = get_spread_start()
        if symbol and price_1 and price_2:
            bot.send_message(message.chat.id,
                             f'Арбитражная возможность для {symbol}: Цена на бирже 1: {price_1}, Цена на бирже 2: {price_2}')
        else:
            bot.send_message(message.chat.id, 'Арбитражных возможностей не найдено.')


    @bot.message_handler(func=lambda message: True)
    def handle_all_messages(message):
        if message.text != 'start':
            bot.send_message(message.chat.id, 'Чтобы начать работу бота введите /start')

    bot.polling(non_stop=True)

if __name__ == '__main__':
    bot()