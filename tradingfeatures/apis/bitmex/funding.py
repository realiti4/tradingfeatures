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

    def get(self, symbol=None, query=None, start=None, end=None, *args, **kwargs):
        start = self.start if start is None else start
        end = time.time() if end is None else end
        start, end = self.to_date(start), self.to_date(end)
        symbol = symbol or 'XBT'
        
        if query is None:
            query = {'symbol': symbol, 'count': self.limit, 'reverse': 'false', 'startTime': start}

        return super(bitmexFunding, self).get(
            query=query,
            start=start,
            end=end,
            *args, **kwargs
        )

    def get_hist(self, convert_funds=False, *args, **kwargs):  
        df_fundings = apiBase.get_hist(
            self,
            columns=['fundingRate', 'fundingRateDaily'],
            interval='8h',
            *args, **kwargs
        )

        # Recent funding
        address = '/instrument'
        r_current = self.get(address=address, query={'symbol': 'XBT'}, return_r=True)
        current_data = r_current.json()[0]

        funding_ts = current_data['fundingTimestamp']
        funding_rate = current_data['fundingRate']
        
        df_recent_funding = pd.DataFrame([[funding_ts, funding_rate]], columns=['timestamp', 'fundingRate'])
        df_recent_funding['timestamp'] = self.to_ts(pd.to_datetime(df_recent_funding['timestamp']))
        df_recent_funding.set_index('timestamp', inplace=True)

        df_final = pd.concat([df_fundings, df_recent_funding])
        df_final = df_final[['fundingRate']]

        if convert_funds:       # convert 8h to 1h and backfill
            aranged_array = np.arange(df_final.index[0], df_final.index[-1] + 1, 3600)
            df_empty = pd.DataFrame(index=aranged_array)
            df_final = df_empty.join(df_final)
            df_final = df_empty.join(df_final).fillna(method='bfill')

        return df_final
