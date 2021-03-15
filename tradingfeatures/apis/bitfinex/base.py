import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase


class bitfinexBase(apiBase):

    def __init__(self):
        super(bitfinexBase, self).__init__(
            name = 'bitfinex',
            per_step = 120,
            sleep = 0.5,
        )

        self.base_address = 'https://api-pub.bitfinex.com/v2'
        self.address = '/candles'
        self.start = 1364778000
        self.limit = 10000
        self.columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']
    
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
            sort = -1,
            ):      
        
        start, end, out_of_range = self.calc_start(limit, start, end)
        if out_of_range:
            return self.get_hist(start=start, end=end)
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'tBTCUSD'        
        
        if query is None:
            limit = self.limit if limit is None else limit
            start, end = self.ts_to_mts(start), self.ts_to_mts(end)     # Conver for Bitfinex
            address = address + f'/trade:{interval}:{symbol}/hist'   

            query = {'limit': limit, 'start': start, 'end': end, 'sort': sort}

        r = self.response_handler(address, params=query, timeout=60)
        
        data = r.json()
        data.reverse()

        df = pd.DataFrame(data, columns=self.columns)
        df['timestamp'] = df['timestamp'].div(1000).astype(int)     # Fixing timestamp inside self.get
        df = df.set_index('timestamp')
        
        if columns is not None:
            return df[columns]
        return df

    def get_hist(self, *args, **kwargs):
        return super(bitfinexBase, self).get_hist(
            *args, **kwargs
        )
    
