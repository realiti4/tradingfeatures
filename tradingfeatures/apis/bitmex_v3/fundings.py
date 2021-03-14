import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitmex_v3.price import bitmexPrice


class bitmexFundings(bitmexPrice):

    def __init__(self):
        super(bitmexFundings, self).__init__()
        self.name = 'bitmex_fundings'

    def get(self, address='funding', *args, **kwargs):
        return super(bitmexFundings, self).get(
            address=address,
            *args, **kwargs
        )

    def get_hist(self, start=1463227200, convert_funds=False, *args, **kwargs):
        df_fundings = apiBase.get_hist(
            self,
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
