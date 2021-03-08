import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import bitfinex
from tradingfeatures import bitstamp
from tradingfeatures import bitmex, bitmex_v2
from tradingfeatures import google_trends


class base:

    def __init__(self):
        self.bitfinex = bitfinex()
        self.bitfinex_wrong = bitfinex(wrong_columns=True)      # Wrong order, keeping for old saved models
        self.bitstamp = bitstamp()
        self.bitmex = bitmex()
        self.bitmex_v2 = bitmex_v2()
        self.google_trends = google_trends()

        self.columns = ['open', 'low', 'high', 'close', 'volume']
        self.columns_final = ['close', 'low', 'high', 'volume', 'fundingRate']

    def eval_get(self, limit=1000, wrong_columns=False):
        if wrong_columns:
            df_bitfinex = self.bitfinex_wrong.get(10000).set_index('timestamp')
        else:
            df_bitfinex = self.bitfinex.get(10000).set_index('timestamp')
        df_bitstamp = self.bitstamp.get(query={'step': 3600, 'limit': 1000}).set_index('timestamp')
        # df_bitmex = self.bitmex.get_funding_rates(save_csv=False)

        self.df1_updated = df_bitfinex[-limit:]
        self.df2_updated = df_bitstamp[-limit:]

        merged = self.uber_get(save=False, update=True, fundings=True, trends=False)        

        return merged
        # return merged[self.columns_final].to_numpy()
        
    def uber_get(self, path='', fundings=False, trends=False, date=True, save=True, update=False, new_api=False):
        if update:
            df1 = self.df1_updated
            df2 = self.df2_updated
        else:
            # df1 = self.bitfinex.get_hist('1h').set_index('timestamp')
            df1 = self.bitfinex.get_hist()
            df2 = self.bitstamp.get_hist()

        # df1.index = df1.index.astype(int)       # fix this in bitfinex later

        df1 = df1[self.columns].loc[:self.current_time()-1]
        df2 = df2[self.columns].loc[:self.current_time()-1]
        
        if save:
            df1.to_csv(path + '/bitfinex_1h.csv')
            df2.to_csv(path + '/bitstamp_1h.csv')
        
        df_temp = df1.join(df2, lsuffix='_bitfinex', rsuffix='_bitstamp')

        df_final = pd.DataFrame(columns=self.columns)
        
        for item in self.columns:
            if item == 'volume':
                df_final[item] = df_temp.loc[:, df_temp.columns.str.contains(item)].sum(axis=1)
            else:
                df_final[item] = df_temp.loc[:, df_temp.columns.str.contains(item)].mean(axis=1)
                
        if date:
            df_final['date'] = pd.to_datetime(df_final.index, unit='s', utc=True)
            
        # Extras
        if fundings:
            final_columns = self.columns
            final_columns.append('fundingRate')
        
            if new_api:
                df_bitmex = self.bitmex_v2.get_fundings()
                merged = self.bitmex_v2.price_funding_merger(df_final, df_bitmex)
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

