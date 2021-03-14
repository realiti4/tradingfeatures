import time
import requests
import pandas as pd

from datetime import datetime

from tradingfeatures import apiBase

class okex(apiBase):

    def __init__(self):
        super(okex, self).__init__(
            name = 'okex',
            per_step = 300,
            sleep = 0,
        )

        self.base_address = 'https://www.okex.com/'

    def get(self,
            limit = 300,
            address = None,
            query = None,
            start = None,
            end = int(time.time()),
            ):

        instrument_id = 'BTC-USD-SWAP'
        address = address or f'api/swap/v3/instruments/{instrument_id}/history/candles'
        address = self.base_address + address

        start, end = self.to_iso(start), self.to_iso(end)

        if query is None:
            query = {'end': end, 'limit': limit}
            if start is not None:
                query['start'] = start

        query = {'start': start, 'limit': limit}
        
        r = self.response_handler(address, params=query, timeout=60)

        # '2021-03-08T20:00:00+00:00' # bizim
        # end.split('+')
        # '2020-07-28T02:31:00.000Z'  # doğru
        
        result = r.json()['data']['ohlc']

        df = pd.DataFrame(result)   # fix index
        df = df.astype(float)
        df['timestamp'] = df['timestamp'].astype(int)

        return df

    def to_iso(self, x):
        x = self.to_date(x)
        x = x.isoformat()
        x = x.split('+')[0] + '.000Z'
        return x
    
    def get_hist(self, *args, **kwargs):
        return super(okex, self).get_hist(            
            start=1514778000,
            name=self.name,
            *args, **kwargs
        )
