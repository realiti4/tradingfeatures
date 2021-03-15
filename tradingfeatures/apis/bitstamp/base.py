import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase


class bitstampBase(apiBase):

    def __init__(self):
        super(bitstampBase, self).__init__(
            name = 'bitstamp',
            per_step = 1000,
            sleep = 0,
        )

        self.base_address = 'https://www.bitstamp.net/api/v2'
        self.address = '/ohlc'
        self.start = 1364778000
        self.limit = 1000
    
    def get(self,
            limit: int = None,
            symbol: str = None,
            address: str = None,
            query: dict = None,
            start: int = None,
            end: int = None,
            interval: str = '1h',
            columns: list = None,
            return_r: bool = False,
            ):

        start, end, out_of_range = self.calc_start(limit, start, end)
        if out_of_range:
            return self.get_hist(start=start, end=end) 
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'btcusd'        
        
        if query is None:
            limit = self.limit if limit is None else limit     
            address = address + f'/{symbol}/'   

            query = {'start': start,'end': end, 'step': 3600, 'limit': limit}

        r = self.response_handler(address, params=query, timeout=60)
        
        result = r.json()['data']['ohlc']

        df = pd.DataFrame(result)   # fix index
        df = df.astype(float)
        df['timestamp'] = df['timestamp'].astype(int)
        df = df.set_index('timestamp')

        if columns is not None:
            return df[columns]
        return df

    def get_hist(self, *args, **kwargs):
        return super(bitstampBase, self).get_hist(
            *args, **kwargs
        )
    
