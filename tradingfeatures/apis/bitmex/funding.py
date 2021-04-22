import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitmex.base import bitmexBase


class bitmexFunding(bitmexBase):

    def __init__(self):
        super(bitmexFunding, self).__init__()
        self.name = 'bitmex_fundings'
        self.address = '/funding'
        self.start = 1463227200
        self.limit = 500
        self.default_columns = ['fundingRate']

    def get(self, 
            limit=None, 
            symbol=None, 
            query=None, 
            start=None, 
            end=None, 
            interval: str = '8h',
            *args, **kwargs
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

        start, end = self.to_date(start), self.to_date(end)
        symbol = symbol or 'XBT'
        
        if query is None:
            query = {'symbol': symbol, 'count': self.limit, 'reverse': 'false', 'startTime': start}

        df = super(bitmexFunding, self).get(
            query=query,
            start=start,
            end=end,
            interval=interval,
            *args, **kwargs
        )

        if get_latest:
            df = self.get_recent(df)

        # check results for get_history with both, solving convert problem here
        # return df
        return self.convert_funding(df, get_latest)

    def get_recent(self, df):   # Recent Funding
        address = '/instrument'
        r_current = super(bitmexFunding, self).get(address=address, query={'symbol': 'XBT'}, return_r=True)
        current_data = r_current.json()[0]

        funding_ts = current_data['fundingTimestamp']
        funding_rate = current_data['fundingRate']
        
        df_recent_funding = pd.DataFrame([[funding_ts, funding_rate]], columns=['timestamp', 'fundingRate'])
        df_recent_funding['timestamp'] = self.to_ts(pd.to_datetime(df_recent_funding['timestamp']))
        df_recent_funding.set_index('timestamp', inplace=True)
        # Compability with other apis, bitmex timestamp indexing is different
        df_recent_funding.index = df_recent_funding.index - 3600

        df_final = pd.concat([df, df_recent_funding])
        df_final = df_final[['fundingRate']]
        
        return df_final

    def get_hist(self, columns=None, convert_funds=False, *args, **kwargs):  
        # columns = ['fundingRate', 'fundingRateDaily'] if columns is None else columns
        return apiBase.get_hist(
            self,
            # columns=columns,
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
        
