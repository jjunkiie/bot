import json
import requests
from config import currencies


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(c_from: str, c_to: str, amount: str):

        if c_from == c_to:
            raise APIException(f'Конвертация одинаковых валют {c_to} не имеет смысла! Результат равен {amount}.')

        try:
            c_from_ticker = currencies[c_from]
        except KeyError:
            raise APIException(f'Неверно указано название валюты {c_from}!')

        try:
            c_to_ticker = currencies[c_to]
        except KeyError:
            raise APIException(f'Неверно указано название валюты {c_to}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неверно указано количество {amount}!')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={c_from_ticker}&tsyms={c_to_ticker}')
        return float(json.loads(r.content)[currencies[c_to]])