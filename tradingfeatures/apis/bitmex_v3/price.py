import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase


class bitmexPrice(apiBase):

    def __init__(self):
        super(bitmexPrice, self).__init__(
            name = 'bitmex',
            per_step = 500,
            sleep = 0,
        )

        self.base_address = 'https://www.bitmex.com/api/v1/'
    
    def get(self,
            address = None,
            query = None,
            start = 1364778000,
            end = int(time.time()),
            interval = '1h',
            return_r = False,
            ):

        address = address or '/trade/bucketed'
        address = self.base_address + address
        symbol = 'XBT'

        start, end = self.to_date(start), self.to_date(end)
        
        if query is None:
            query = {'symbol': symbol, 'count': 500, 'reverse': 'false', 'startTime': start}
            if '/trade' in address:
                query['binSize'] = interval

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
        # df = df.astype(float)

        # int timestamp, and float convertion here

        return df

    def get_hist(self, start=1423186000, *args, **kwargs):
        return super(bitmexPrice, self).get_hist(
            address='/trade/bucketed',
            start=start,
            name=self.name,
            *args, **kwargs
        )
