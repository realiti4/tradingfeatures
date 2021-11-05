import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.binance.base import binanceBase


class binanceOrderBook(binanceBase):

    def __init__(self):
        super(binanceOrderBook, self).__init__()
        self.name = 'binance_orderbook'
        self.base_address = 'https://api.binance.com'
        self.address = '/api/v3/depth'
        self.start = 1568002400
        self.limit = 5000
        self.per_step = 500
    
    def get(self,
            limit: int = None,          # Default 100; max 5000. Valid limits:[5, 10, 20, 50, 100, 500, 1000, 5000]
            symbol: str = None,
            address: str = None,
            query: dict = None,
            group_by: int = None,
            columns: list = None,
            return_r: bool = False,
            ):
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'BTCUSDT'
        
        if query is None:
            query = {'symbol': symbol, 'limit': limit}

        r = self.response_handler(address, query)

        result = r.json()
        # df = pd.DataFrame(result)

        # Try something new
        bids = pd.DataFrame(result['bids'], columns=['price', 'amount'], dtype=np.float32)
        asks = pd.DataFrame(result['asks'], columns=['price', 'amount'], dtype=np.float32)

        # Group and sum
        def group(df, group_by=100):
            ds = (df.index.to_series() / group_by).astype(int)     # downsample
            return df.groupby(ds).agg({'price': 'mean', 'amount': 'sum'})

        if group_by:
            return group(bids, group_by), group(asks, group_by)
        else:

            return bids, asks


        return df

class binanceRecentTrades(binanceBase):

    def __init__(self):
        super(binanceRecentTrades, self).__init__()
        self.name = 'binance_recenttrades'
        self.base_address = 'https://api.binance.com'
        self.address = '/api/v3/trades'
        self.limit = 1000
    
    def get(self,
            limit: int = None,          # Default 500; max 1000.
            symbol: str = None,
            address: str = None,
            query: dict = None,
            return_r: bool = False,
            ):
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'BTCUSDT'
        
        if query is None:
            query = {'symbol': symbol, 'limit': limit}

        r = self.response_handler(address, query)

        result = r.json()
        df = pd.DataFrame(result)

        return df