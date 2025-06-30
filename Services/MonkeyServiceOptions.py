from datetime import timedelta
from Globals.Constants import CACHE_EXPIRATION_TIME


class MonkeyServiceOptions:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.cache_expiration = timedelta(minutes=CACHE_EXPIRATION_TIME)