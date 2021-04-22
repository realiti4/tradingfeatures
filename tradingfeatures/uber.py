import os
import time
import requests
import numpy as np
import pandas as pd

from concurrent.futures import ThreadPoolExecutor, as_completed
from tradingfeatures import bitfinex, bitstamp, bitmex, binance
from tqdm.contrib.concurrent import thread_map


class Uber:

    def __init__(self,
        api_to_use: list = ['bitfinex', 'bitstamp'],
        columns: bool = None,
        column_kwargs: dict = None,
        ):

        self.apis_dict = {
            'bitfinex': bitfinex(),
            'bitstamp': bitstamp(),            
            'binance': binance(),
            'binance_funding': binance().funding,
            'bitmex': bitmex(),
            'bitmex_funding': bitmex().funding,
            'bitmex_quote': bitmex().quote,
        }

        self.apis = [self.apis_dict.get(key) for key in api_to_use]

        self.bitmex = bitmex()
        # self.google_trends = google_trends()

        self.columns = ['open', 'low', 'high', 'close', 'volume'] if columns is None else columns
        self.column_kwargs = {} if column_kwargs is None else column_kwargs

    def eval_get(self, limit=1000, **kwargs):
        futures = []

        with ThreadPoolExecutor(8) as executor:
            for api in self.apis:
                api_columns = self.column_kwargs[api.name] if api.name in self.column_kwargs else None
                future = executor.submit(api.get, limit=limit, columns=api_columns, **kwargs)
                futures.append([api.name, future])

        datasets = [[item[0], item[1].result()[-limit:]] for item in futures]

        merged = self.get(datasets=datasets, save=False, trends=False, date=False, **kwargs)

        # Fix for 0 and nan - check here again later
        merged = merged.replace(0, np.nan)
        if merged.isnull().values.any():    # Check here later
            merged = merged.interpolate()

        return merged
        
    def get(self, path='', datasets=None, merge=True, trends=False, date=True, 
            save=True, **kwargs):
        
        if datasets is None:    # if dataset update, else download everything
            futures = []
            with ThreadPoolExecutor(4) as executor:
                for api in self.apis:
                    api_columns = self.column_kwargs[api.name] if api.name in self.column_kwargs else None
                    future = executor.submit(api.get_hist, **kwargs)
                    futures.append([api.name, future])

            datasets = [[item[0], item[1].result()] for item in futures]
        
        assert isinstance(datasets[0], list) and len(datasets[0]) == 2, "Use a list of list like [[api_name, api_df], ..]"
        
        # Remove active hour and fix columns
        for i in range(len(datasets)):
            api_name = datasets[i][0]
            api_columns = self.column_kwargs[api_name] if api_name in self.column_kwargs else None
            if api_columns is None:
                datasets[i][1] = datasets[i][1].loc[:self.current_time()-1]
            else:
                datasets[i][1] = datasets[i][1][api_columns].loc[:self.current_time()-1]

        if save:    # Maybe save above after just getting history
            for df in datasets:
                name, df = df[0], df[1]
                df.to_csv(path + f'/{name}.csv')
        if not merge:
            return

        # # Join one dataset at a time
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
            if item == 'volume' or item == 'trades':
                df_final[item] = df_main.loc[:, df_main.columns.str.contains(item)].sum(axis=1)
            else:
                df_final[item] = df_main.loc[:, df_main.columns.str.contains(item)].mean(axis=1)
                
        if date:
            df_final['date'] = pd.to_datetime(df_final.index, unit='s', utc=True)            

        if trends:
            df_trends = self.google_trends.update('uber_data')
            df_final = df_final.join(df_trends)

            df_final['google_trends'].replace(0, np.nan, inplace=True)
            df_final['google_trends'] = df_final['google_trends'].astype(float).interpolate()            
        
        if save:
            df_final.to_csv(path + '/merged_final.csv')
        
        return df_final
        
    def update(self, path='uber_data', **kwargs):  # Fix path
        working_directory = os.getcwd()
        datasets = []

        for api in self.apis:
            path_df = path + f'/{api.name}.csv'
            # df = pd.read_csv(path_df, index_col=0)
            # datasets.append([api.name, df])
            # # break

            if os.path.exists(path_df):
                df = api.update(path_df)
            else:
                print(f"Couldn't find {api.name} data, downloading from strach..")
                raise Exception
                # df = api.get_hist()
                # df.to_csv(path_df)

            datasets.append([api.name, df])

        updated = self.get(path, datasets=datasets, save=False, **kwargs)
        updated.to_csv(path + '/merged_final.csv')
        return

    def current_time(self):        
        return int((time.time() // 3600) * 3600)     # Hourly current time

