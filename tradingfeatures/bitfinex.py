import time
import requests
import pandas as pd

from datetime import datetime

from tradingfeatures import apiBase

class bitfinex(apiBase):
    
    def __init__(self, wrong_columns=False):
        super(bitfinex, self).__init__(
            name = 'bitfinex',
            per_step = 120,
            sleep = 0.5,
        )

        if wrong_columns:
            # Wrong order that I accidently trained
            self.columns = ['timestamp', 'open', 'low', 'high', 'close', 'volume']
        else:
            self.columns = ['timestamp', 'open', 'close', 'high', 'low', 'volume']

        self.times_dict = {'5m': 5, '15m': 15, '30m': 30, '1h': 60, '3h': 180, '6h': 360, '12h': 720}

    def get(self,
            limit = None,
            address = None,
            query = None,
            start = None,
            end = int(time.time()),
            timeframe = '1h',
            currency_pair = 'tBTCUSD',
            sort = -1,
            ):
        
        start, end = self.timestamp_mts(start), self.timestamp_mts(end)     # Conver for Bitfinex

        address = f'https://api-pub.bitfinex.com/v2/candles/trade:{timeframe}:{currency_pair}/hist'
        query = {'limit': limit, 'end': end, 'sort': sort}
        if start is not None:
            query['start'] = start    

        r = self.response_handler(address, params=query, timeout=60)
        
        data = r.json()
        data.reverse()

        df = pd.DataFrame(data, columns=self.columns)
        df['timestamp'] = df['timestamp'].div(1000).astype(int)     # Fixing timestamp inside self.get
        
        return df

    def get_hist(self, *args, **kwargs):
        return super(bitfinex, self).get_hist(            
            get=self.get,
            start=1364778000,
            name=self.name,
            *args, **kwargs
        )

    def timestamp_mts(self, time):
        # second timestamp to millisecond timestamp
        if time:
            if len(str(time)) == 10:
                return int(time)*1000
            else:
                assert len(str(time)) == 13, 'Please use a timestamp value with lenght 10!'
                return int(time)