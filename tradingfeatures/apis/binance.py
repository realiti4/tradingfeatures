import time
import requests
import pandas as pd

from datetime import datetime

from tradingfeatures import apiBase

class binance(apiBase):

    def __init__(self):
        super(binance, self).__init__(
            name = 'binance',
            per_step = 1000,
            sleep = 0.7,
        )

        self.base_address = 'https://api.binance.com'

    # def get(self, start=1484778000, end=int(time.time())):
    def get(self,
            limit = 1000,
            address = None,
            query = None,
            start = None,
            end = int(time.time()),
            ):

        start, end = self.ts_to_mts(start), self.ts_to_mts(end)
        currency_pair = 'BTCUSDT'
        address = address or '/api/v3/klines'
        address = self.base_address + address
        
        if query is None:
            query = {'symbol': currency_pair, 'interval': '1h', 'endTime': end, 'limit': limit}
            if start is not None:
                query['startTime'] = start

        r = requests.get(address, params=query)

        result = r.json()

        df = pd.DataFrame(result, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                                    'number_of_trades', 'taker_base_asset_volume', 'taker_quote_asset_volume', 'ignore'])

        df = df.astype(float)
        df['timestamp'] = df['open_time'].div(1000).astype(int)
        df.pop('open_time')
        df.pop('close_time')
        df.pop('ignore')

        return df.astype(float)

    def get_hist(self, *args, **kwargs):
        return super(binance, self).get_hist(
            start=1500000000,         
            # start=1484778000,
            name=self.name,
            *args, **kwargs
        )

    def ts_to_mts(self, time):
        # second timestamp to millisecond timestamp
        if time:
            if len(str(time)) == 10:
                return int(time)*1000
            else:
                assert len(str(time)) == 13, 'Please use a timestamp value with lenght 10!'
                return int(time)
    
    
