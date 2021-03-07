import time
import requests
import pandas as pd

from datetime import datetime

from tradingfeatures import apiBase

class bitstamp(apiBase):

    def __init__(self):
        super(bitstamp, self).__init__(
            name = 'bitstamp_1h',
            per_step = 1000,
            sleep = 0,
        )

    def get(self, start=1364778000, end=int(time.time()), query=None):
        currency_pair = 'btcusd'
        address = f'https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/'

        if query is None:
            query = {'start': start, 'end': end, 'step': 3600, 'limit': 1000}        
        
        r = self.response_handler(address, params=query, timeout=60)
        
        result = r.json()['data']['ohlc']

        df = pd.DataFrame(result)   # fix index
        df = df.astype(float)
        df['timestamp'] = df['timestamp'].astype(int)

        return df
