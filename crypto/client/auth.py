import requests


class BinanceHook:
    """A basic binance hook
    """
    BASIC_URL = "https://api3.binance.com"

    def __init__(self, **kwargs):
        self.auth = kwargs.get('auth', None)
        self.client = requests.Session()
