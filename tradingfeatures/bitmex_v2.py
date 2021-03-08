import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase


class bitmex_v2(apiBase):

    def __init__(self):
        super(bitmex_v2, self).__init__(
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
            return_r = False,
            ):

        address = address or 'funding'
        address = self.base_address + address
        symbol = 'XBT'

        start, end = self.to_date(start), self.to_date(end)
        
        if query is None:
            query = {'symbol': symbol, 'count': 500, 'reverse': 'false', 'startTime': start}

        r = self.response_handler(address, query)
        # Bitmex remaining limit
        if 'x-ratelimit-remaining' in r.headers:
            if int(r.headers['x-ratelimit-remaining']) <= 1:
                print('reached the rate limit, bitmex api is sleeping...')
                time.sleep(61)
        if return_r:
            return r

        df_fundings = pd.read_json(r.content)
        df_fundings['timestamp'] = self.to_ts(df_fundings['timestamp'])

        return df_fundings

    def get_test(self):
        self.get(address='instrument', query={'symbol': 'XBT'})

    def get_fundings(self, *args, **kwargs):

        df_fundings = super(bitmex_v2, self).get_hist(
            name='bitmex_funding',
            get=self.get,
            start=1463227200,
            columns=['timestamp', 'fundingRate', 'fundingRateDaily'],
            interval='8h',
            *args, **kwargs
        )

        # Recent funding
        address = 'instrument'
        r_current = self.get(address, query={'symbol': 'XBT'}, return_r=True)
        current_data = r_current.json()[0]

        funding_ts = current_data['fundingTimestamp']
        funding_rate = current_data['fundingRate']
        
        df_recent_funding = pd.DataFrame([[funding_ts, funding_rate]], columns=['timestamp', 'fundingRate'])
        df_recent_funding['timestamp'] = self.to_ts(pd.to_datetime(df_recent_funding['timestamp']))
        df_recent_funding.set_index('timestamp', inplace=True)

        df_final = pd.concat([df_fundings, df_recent_funding])
        df_final = df_final[['fundingRate']]

        return df_final

    def price_funding_merger(self, df, df_fundings):
        aranged_array = np.arange(df_fundings.index[0], df_fundings.index[-1] + 1, 3600)
        df_empty = pd.DataFrame(index=aranged_array)

        df_fundings = df_empty.join(df_fundings)
        df_fundings = df_empty.join(df_fundings).fillna(method='bfill')   # can remove limit
        # df_fundings['fundingRate'].replace(0, 0.0001, inplace=True)     # Check this
        
        merged = df.join(df_fundings)

        return merged, df_fundings   
