import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase


class bitmexBase(apiBase):

    def __init__(self):
        super(bitmexBase, self).__init__(
            name = 'bitmex',
            per_step = 500,
            sleep = 0,
        )

        self.base_address = 'https://www.bitmex.com/api/v1'
        self.address = '/trade/bucketed'
        self.start = 1423227200
        self.limit = 500
    
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

        start, end, out_of_range = self.calc_start(limit, start, end, interval)
        if out_of_range:
            return self.get_hist(start=start, end=end, columns=columns)
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'XBT'
        
        if query is None:
            limit = self.limit if limit is None else limit
            start, end = self.to_date(start), self.to_date(end)

            query = {'symbol': symbol, 'binSize': interval, 'count': limit, 'startTime': start, 'endTime': end,
                    'reverse': 'false'}

        r = self.response_handler(address, query)
        # Bitmex remaining limit
        if 'x-ratelimit-remaining' in r.headers:
            if int(r.headers['x-ratelimit-remaining']) <= 1:
                print('\nreached the rate limit, bitmex api is sleeping...')
                time.sleep(61)
        if return_r:
            return r

        df = pd.read_json(r.content)
        df['timestamp'] = self.to_ts(df['timestamp'])
        df.pop('symbol')
        df = df.set_index('timestamp')
        df.index = df.index.astype(int)
        # df = df.astype(float)

        df.index = df.index - 3600  # Compability with other apis, bitmex timestamp indexing is different
        if columns is not None:
            return df[columns]
        return df

    def get_hist(self, *args, **kwargs):
        return super(bitmexBase, self).get_hist(
            *args, **kwargs
        )
