import json
import requests

from CONFIG import keys
from CONFIG import API_TOKEN

class ConvExc(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base:str, amount: str):
        if quote == base:
            raise ConvExc(f'Нельзя конвертировать одинаковые валюты {base}')

        try:
            quote_tick = keys[quote]
        except KeyError:
            raise ConvExc(f'не удалось обработать валюту {quote}')

        try:
            base_tick = keys[base]
        except KeyError:
            raise ConvExc(f'не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvExc(f'не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tick}&tsyms={base_tick}')
  #      r = requests.get(f'https://free.currconv.com/api/v7/convert?q={quote_tick}_{base_tick}&apiKey={API_TOKEN}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base

