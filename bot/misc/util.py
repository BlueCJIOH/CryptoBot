import requests

exchange_list = list(map(lambda el: el['name'], requests.get("http://web:8000/exchanges/").json())) + ["Common log", ]