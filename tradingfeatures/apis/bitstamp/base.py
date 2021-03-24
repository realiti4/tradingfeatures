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

        self.symbol_dict = {
            'btcusd': 'btcusd',
            'ethusd': 'ethusd',
            'ethbtc': 'ethbtc',
            'ltcusd': 'ltcusd',
            'bchusd': 'bthusd',
            'eosusd': 'eosusd',
            'xrpusd': 'xrpusd',
        }
    
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

        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'btcusd'        

        start, end, out_of_range = self.calc_start(limit, start, end)
        if out_of_range:
            return self.get_hist(symbol=symbol, start=start, end=end)

        symbol = self.symbol_check(symbol)  # had to give raw symbol above, this has to be after
        
        if query is None:
            limit = self.limit if limit is None else limit     
            address = address + f'/{symbol}/'

            query = {'start': start,'end': end, 'step': 3600, 'limit': limit}

        r = self.response_handler(address, params=query, timeout=60)
        
        result = r.json()['data']['ohlc']
        if len(result) == 0:
            return None

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

    def _start_check(self, address, symbol):
        raise Exception('Cant sort oldest item')
    
