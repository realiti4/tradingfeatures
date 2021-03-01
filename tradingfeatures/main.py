import time
import requests
import pandas as pd

from tradingfeatures import bitfinex
from tradingfeatures import bitstamp
from tradingfeatures import bitmex
from tradingfeatures import google_trends


class base:

    def __init__(self):
        self.bitfinex = bitfinex()
        self.bitmex = bitmex()

        self.columns = ['close', 'low', 'high', 'volume', 'fundingRate']

    def get(self, limit=10000):
        df_bitfinex = self.bitfinex.get(10000)
        df_bitmex = self.bitmex.get_funding_rates(save_csv=False)

        merged = self.bitmex.price_funding_merger(df_bitfinex, df_bitmex)

        merged = merged[self.columns]

        return merged.to_numpy()
        
class base_v2:

    def __init__(self):
        self.bitfinex = bitfinex()
        self.bitstamp = bitstamp()
        self.bitmex = bitmex()

        self.columns = ['open', 'low', 'high', 'close', 'volume']
        self.columns_final = ['close', 'low', 'high', 'volume', 'fundingRate']

    def eval_get(self, limit=1000):
        df_bitfinex = self.bitfinex.get(10000).set_index('timestamp')
        df_bitstamp = self.bitstamp.get(query={'step': 3600, 'limit': 1000}).set_index('timestamp')
        # df_bitmex = self.bitmex.get_funding_rates(save_csv=False)

        self.df1_updated = df_bitfinex[-limit:]
        self.df2_updated = df_bitstamp[-limit:]

        merged = self.uber_get(save=False, update=True, fundings=True)        

        return merged[self.columns_final].to_numpy()
        
    def uber_get(self, path='', fundings=False, date=True, save=True, update=False):
        if update:
            df1 = self.df1_updated
            df2 = self.df2_updated
        else:
            df1 = self.bitfinex.get_hist('1h').set_index('timestamp')
            df2 = self.bitstamp.get_hist().set_index('timestamp')

        df1.index = df1.index.astype(int)
        # df2.index = df2.index.astype(int)
        
        df1 = df1[self.columns]
        df2 = df2[self.columns]
        
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
            
        if fundings:
            final_columns = self.columns
            final_columns.append('fundingRate')
        
            df_bitmex = self.bitmex.get_funding_rates(save_csv=False)
            
            merged = self.bitmex.price_funding_merger(df_final, df_bitmex)
            df_final = merged[final_columns]
            
        return df_final
        
    def uber_update(self, path, fundings):
        bitfinex_path = path + '/bitfinex_1h.csv'
        bitstamp_path = path + '/bitstamp_1h.csv'         
    
        self.bitfinex.update_csv(bitfinex_path, alternative_mode=True)
        self.bitstamp.update(bitstamp_path)
        
        self.df1_updated = pd.read_csv(bitfinex_path, index_col='timestamp')
        self.df2_updated = pd.read_csv(bitstamp_path, index_col='timestamp')
        
        updated = self.uber_get(path, fundings, update=True)
        
        updated.to_csv(path + '/merged_1h.csv')

# base = base()

# test = base.get()

# test.to_csv('testtest.csv', index=False)