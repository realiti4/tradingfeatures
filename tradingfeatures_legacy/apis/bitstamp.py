import time
import requests
import pandas as pd

from datetime import datetime

from tradingfeatures_legacy import apiBase

class bitstampLegacy(apiBase):

    def __init__(self):
        super(bitstampLegacy, self).__init__(
            name = 'bitstamp',
            per_step = 1000,
            sleep = 0,
        )

        self.base_address = 'https://www.bitstamp.net/api/v2/'

    def get(self,
            limit = 1000,
            address = None,
            query = None,
            start = None,
            end = int(time.time()),
            ):

        currency_pair = 'btcusd'
        address = address or f'https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/'

        if query is None:
            query = {'end': end, 'step': 3600, 'limit': limit}
            if start is not None:
                query['start'] = start
        
        r = self.response_handler(address, params=query, timeout=60)
        
        result = r.json()['data']['ohlc']

        df = pd.DataFrame(result)   # fix index
        df = df.astype(float)
        df['timestamp'] = df['timestamp'].astype(int)

        return df

    def get_hist(self, start=1364778000, *args, **kwargs):
        return super(bitstampLegacy, self).get_hist(            
            start=start,
            name=self.name,
            *args, **kwargs
        )
