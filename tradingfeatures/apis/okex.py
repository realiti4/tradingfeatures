import time
import requests
import pandas as pd

from datetime import datetime

from tradingfeatures import apiBase

class okex(apiBase):

    def __init__(self):
        super(okex, self).__init__(
            name = 'okex',
            per_step = 1000,
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

        end = self.to_date(end)
        end = end.isoformat()
        end = end.split('+')[0] + '.000Z'

        if query is None:
            query = {'end': end, 'limit': limit}
            if start is not None:
                query['start'] = start
        
        r = self.response_handler(address, params=query, timeout=60)

        # '2021-03-08T20:00:00+00:00' # bizim
        # end.split('+')
        # '2020-07-28T02:31:00.000Z'  # doğru
        
        result = r.json()['data']['ohlc']

        df = pd.DataFrame(result)   # fix index
        df = df.astype(float)
        df['timestamp'] = df['timestamp'].astype(int)

        return df

    def get_hist(self, *args, **kwargs):
        return super(bitstamp, self).get_hist(            
            start=1364778000,
            name=self.name,
            *args, **kwargs
        )
