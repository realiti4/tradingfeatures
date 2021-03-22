import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.binance.base import binanceBase


class binanceOrderBook(binanceBase):

    def __init__(self):
        super(binanceOrderBook, self).__init__()
        self.name = 'binance_orderbook'
        self.base_address = 'https://api.binance.com'
        self.address = '/api/v3/depth'
        self.start = 1568002400
        self.limit = 5000
        self.per_step = 500
    
    def get(self,
            limit: int = None,
            symbol: str = None,
            address: str = None,
            query: dict = None,
            columns: list = None,
            return_r: bool = False,
            ):
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'BTCUSDT'        
        
        if query is None:
            query = {'symbol': symbol, 'limit': limit}

        r = self.response_handler(address, query)

        result = r.json()
        df = pd.DataFrame(result)

        return df