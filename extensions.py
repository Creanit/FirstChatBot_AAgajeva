import requests
import json
from config import keys

class APIException(Exception):
    pass

class ServerException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise APIException(f'Не удалось перевести одинаковые валюты {base}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Некорректное количество валюты - {amount}. Возможно надо использовать точку, а не запятую (пример: 10.5).')

        if amount <= 0:
            raise APIException("Количество валюты должно быть больше нуля.")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        data = json.loads(r.content)

        try:
            rate = data[quote_ticker]
            total_base = round(rate * amount, 4)
        except (KeyError, TypeError):
            raise ServerException('Ошибка при получении данных с сервера. Попробуйте позже.')

        return (f"Курс: 1 {base.upper()} = {rate:.2f} {quote.upper()}\n"
                f"Итого: {float(amount):.2f} {base.lower()} = {total_base:.2f} {quote.lower()}")