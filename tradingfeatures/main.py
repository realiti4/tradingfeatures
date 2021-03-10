import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import bitfinex
from tradingfeatures import bitstamp
from tradingfeatures import bitmex, bitmex_v2
from tradingfeatures import binance
from tradingfeatures import google_trends


class base:

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

    def eval_get(self, limit=1000, new_api=False, wrong_columns=False):
        datasets = []

        for api in self.apis:
            df = api.get().set_index('timestamp')
            df = df[-limit:]
            datasets.append([api.name, df])

        # self.bitstamp.get(query={'step': 3600, 'limit': 1000}).set_index('timestamp')

        merged = self.uber_get(datasets=datasets, save=False, fundings=True, trends=False, new_api=new_api)
        return merged

        if wrong_columns:
            df_bitfinex = self.bitfinex_wrong.get(10000).set_index('timestamp')
        else:
            df_bitfinex = self.bitfinex.get(10000).set_index('timestamp')
        df_bitstamp = self.bitstamp.get(query={'step': 3600, 'limit': 1000}).set_index('timestamp')
        # df_bitmex = self.bitmex.get_funding_rates(save_csv=False)

        self.df1_updated = df_bitfinex[-limit:]
        self.df2_updated = df_bitstamp[-limit:]

        merged = self.uber_get(save=False, update=True, fundings=True, trends=False, new_api=new_api)

        return merged        
        
    def uber_get(self, path='', datasets=None, merge=True, fundings=False, trends=False, date=True, save=True, update=False, 
                new_api=False):
        
        if datasets is None:    # if dataset update, else download everything
            datasets = []

            for api in self.apis:
                # hist = api.get_hist()
                df = api.get().set_index('timestamp')
                datasets.append([api.name, df])

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
        
    def uber_update(self, path, fundings=True):
        bitfinex_path = path + '/bitfinex_1h.csv'
        bitstamp_path = path + '/bitstamp_1h.csv'         
    
        # self.bitfinex.update_csv(bitfinex_path, alternative_mode=True)
        self.bitfinex.update(bitfinex_path)
        self.bitstamp.update(bitstamp_path)
        
        self.df1_updated = pd.read_csv(bitfinex_path, index_col='timestamp')
        self.df2_updated = pd.read_csv(bitstamp_path, index_col='timestamp')
        
        updated = self.uber_get(path, fundings, update=True)
        
        updated[:-1].to_csv(path + '/merged_1h.csv')

    def current_time(self):        
        return int((time.time() // 3600) * 3600)     # Hourly current time

