import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase


class bitmex(apiBase):

    def __init__(self):
        super(bitmex, self).__init__(
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
        return super(bitmex, self).get_hist(
            address='/trade/bucketed',
            start=start,
            name=self.name,
            *args, **kwargs
        )

    def get_quote(self, start=1423186000, *args, **kwargs):
        return super(bitmex, self).get_hist(
            address='/quote/bucketed',
            start=start,
            name=self.name,
            *args, **kwargs
        )

        address = '/quote/bucketed'
        self.get(address='instrument', query={'symbol': 'XBT'})

    def get_settlement(self):
        return

    def get_fundings(self, start=1463227200, convert_funds=False, *args, **kwargs):
        df_fundings = super(bitmex, self).get_hist(
            name='bitmex_funding',
            address='funding',
            start=start,
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

        if convert_funds:       # convert 8h to 1h and backfill
            aranged_array = np.arange(df_final.index[0], df_final.index[-1] + 1, 3600)
            df_empty = pd.DataFrame(index=aranged_array)
            df_final = df_empty.join(df_final)
            df_final = df_empty.join(df_final).fillna(method='bfill')

        return df_final

    # def price_funding_merger(self, df, df_fundings):
    #     aranged_array = np.arange(df_fundings.index[0], df_fundings.index[-1] + 1, 3600)
    #     df_empty = pd.DataFrame(index=aranged_array)

    #     df_fundings = df_empty.join(df_fundings)
    #     df_fundings = df_empty.join(df_fundings).fillna(method='bfill')   # can remove limit
    #     # df_fundings['fundingRate'].replace(0, 0.0001, inplace=True)     # Check this
        
    #     merged = df.join(df_fundings)

    #     return merged, df_fundings   
