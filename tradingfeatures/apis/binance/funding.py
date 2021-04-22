import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.binance.base import binanceBase


class binanceFunding(binanceBase):

    def __init__(self):
        super(binanceFunding, self).__init__()
        self.name = 'binance_fundings'
        self.base_address = 'https://fapi.binance.com'
        self.address = '/fapi/v1/fundingRate'
        self.start = 1568002400
        self.limit = 500
        self.per_step = 500
    
    def get(self,
            limit: int = None,
            symbol: str = None,
            address: str = None,
            query: dict = None,
            start: int = None,
            end: int = None,
            interval: str = '8h',
            columns: list = None,
            return_r: bool = False,
            ):

        assert interval == '8h'
        start, end, out_of_range = self.calc_start(limit, start, end, interval, scale=8)
        if out_of_range:
            return self.get_hist(start=start, end=end)

        # Get recent funding if getting latest data
        if (int(end) // 3600) *3600 == (time.time() // 3600) *3600:
            get_latest = True
        else:
            get_latest = False
        
        address = address or self.address
        address = self.base_address + address
        symbol = symbol or 'btcusd'
        symbol = self.symbol_dict[symbol]    
        
        if query is None:
            limit = self.limit if limit is None else limit
            start, end = self.ts_to_mts(start), self.ts_to_mts(end)

            query = {'symbol': symbol, 'startTime': start, 'endTime': end, 'limit': self.limit}

        r = self.response_handler(address, query)

        result = r.json()

        df = pd.DataFrame(result)
        df['timestamp'] = df['fundingTime'].div(1000).astype(int)
        df.pop('fundingTime')
        df.pop('symbol')
        df = df.set_index('timestamp')
        df = df.astype(float)
        df.rename(columns={'fundingRate': 'fundingRate_binance'}, inplace=True)   
        
        if get_latest:      # add this to binance as well
            df = self.get_recent(df)
        
        # if columns is not None:
        #     return df[columns]
        return self.convert_funding(df, get_latest)

    def get_recent(self, df):
        address = '/fapi/v1/premiumIndex'
        address = self.base_address + address

        r = self.response_handler(address, params={'symbol': 'BTCUSDT'})
        result = r.json()
        df_temp = pd.DataFrame([[result['nextFundingTime'], result['lastFundingRate']]], columns=['timestamp', 'fundingRate_binance'])
        df_temp = df_temp.set_index(df_temp['timestamp'].div(1000).astype(int))
        df_temp.pop('timestamp')
        df = pd.concat([df, df_temp])

        return df

    def get_hist(self, columns=None, *args, **kwargs):
        columns = ['fundingRate_binance'] if columns is None else columns
        return apiBase.get_hist(
            self,
            columns=columns,
            interval='8h',
            *args, **kwargs
        )

    def convert_funding(self, df, get_latest=False):  # convert 8h to 1h and backfill        
        if not get_latest:
            aranged_array = np.arange(df.index[0], (df.index[-1] + (8*3600)), 3600)
        else:
            aranged_array = np.arange(df.index[0], df.index[-1] + 1, 3600)

        df_empty = pd.DataFrame(index=aranged_array)
        df = df_empty.join(df)
        df = df_empty.join(df).fillna(method='bfill')
        return df