import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase


class binanceBase(apiBase):

    def __init__(self):
        super(binanceBase, self).__init__(
            name = 'binance',
            per_step = 1000,
            sleep = 0.7,
        )

        self.base_address = 'https://api.binance.com'
        self.address = '/api/v3/klines'
        self.start = 1364778000
        self.limit = 1000
    
    def get(self,
            limit: int = None,
            symbol: str = None,
            address: str = None,
            query: dict = None,
            start: int = None,
            end: int = None,
            interval: str = '1h',
            return_r: bool = False,
            ):      
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'BTCUSDT'        
        
        if query is None:
            limit = self.limit if limit is None else limit
            start, end = self.ts_to_mts(start), self.ts_to_mts(end)

            query = {'symbol': symbol, 'interval': interval, 'endTime': end, 'limit': limit}
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
        # start = 1500000000
        return super(binanceBase, self).get_hist(
            *args, **kwargs
        )
    