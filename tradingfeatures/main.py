import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import bitfinex
from tradingfeatures import bitstamp
from tradingfeatures import bitmex, bitmex_v2
from tradingfeatures import binance
from tradingfeatures import google_trends


class uber:

    def __init__(self,
        api_to_use=['bitfinex', 'bitstamp']
        ):

        self.apis_dict = {
            'bitfinex': bitfinex(),
            'bitfinex_wrong': bitfinex(wrong_columns=True),
            'bitstamp': bitstamp(),
            'bitmex': bitmex(),
            'bitmex_v2': bitmex_v2(),
            'binance': binance(),
        }

        self.apis = [self.apis_dict.get(key) for key in api_to_use]

        self.bitmex = bitmex()
        self.bitmex_v2 = bitmex_v2()
        self.google_trends = google_trends()

        self.columns = ['open', 'low', 'high', 'close', 'volume']
        self.columns_final = ['close', 'low', 'high', 'volume', 'fundingRate']

    def eval_get(self, limit=1000, new_api=False):
        datasets = []

        for api in self.apis:
            df = api.get().set_index('timestamp')
            df = df[-limit:]
            datasets.append([api.name, df])

        merged = self.get(datasets=datasets, save=False, fundings=True, trends=False, new_api=new_api)
        return merged
        
    def get(self, path='', datasets=None, merge=True, fundings=False, trends=False, date=True, save=True, 
                new_api=False):
        
        if datasets is None:    # if dataset update, else download everything
            datasets = []

            for api in self.apis:
                df = api.get_hist()                
                datasets.append([api.name, df])        
        
        assert isinstance(datasets[0], list) and len(datasets[0]) == 2, "Use a list of list like [[api_name, api_df], ..]"
        
        for i in range(len(datasets)):
            datasets[i][1] = datasets[i][1][self.columns].loc[:self.current_time()-1]

        if save:
            for df in datasets:
                name, df = df[0], df[1]
                df.to_csv(path + f'/{name}_1h.csv')
        if not merge:
            return

        # # And find a find to join more than 2 datasets each at a time. maybe an outer function might help
        name_main, df_main = datasets[0]
        for i in range(1, len(datasets)):
            name = datasets[i][0]
            df_join = datasets[i][1]
            if i == 1:
                df_main = df_main.join(df_join, lsuffix=f'_{name_main}', rsuffix=f'_{name}')
            else:
                df_main = df_main.join(df_join, rsuffix=f'_{name}')

        df_final = pd.DataFrame(columns=self.columns)
        
        for item in self.columns:
            if item == 'volume':
                df_final[item] = df_main.loc[:, df_main.columns.str.contains(item)].sum(axis=1)
            else:
                df_final[item] = df_main.loc[:, df_main.columns.str.contains(item)].mean(axis=1)
                
        if date:
            df_final['date'] = pd.to_datetime(df_final.index, unit='s', utc=True)
            
        # Extras
        if fundings:
            final_columns = self.columns
            final_columns.append('fundingRate')
        
            if new_api:
                start_timestamp = df_final.index[0]
                df_bitmex = self.bitmex_v2.get_fundings(start_timestamp)  
                merged, df_bitmex = self.bitmex_v2.price_funding_merger(df_final, df_bitmex)
                if save:
                    df_bitmex.to_csv(path + '/bitmex_fundings.csv')
            else:
                df_bitmex = self.bitmex.get_funding_rates(save_csv=False)            
                merged = self.bitmex.price_funding_merger(df_final, df_bitmex)

            df_final = merged[final_columns]

        if trends:
            df_trends = self.google_trends.update('uber_data')
            df_final = df_final.join(df_trends)

            df_final['google_trends'].replace(0, np.nan, inplace=True)
            df_final['google_trends'] = df_final['google_trends'].astype(float).interpolate()            
        
        if save:
            df_final.to_csv(path + '/merged_final.csv')
        
        return df_final
        
    def update(self, path, fundings=True):
        datasets = []

        for api in self.apis:
            path_df = f'/{api.name}_1h.csv'
            df = api.update(path_df)

            datasets.append([api.name, df])

        updated = self.get(path, datasets=datasets, fundings=fundings)
        updated.to_csv(path + '/merged_1h.csv')
        return

    def current_time(self):        
        return int((time.time() // 3600) * 3600)     # Hourly current time

