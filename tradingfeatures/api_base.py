import os
import time
import logging, sys
import requests
import numpy as np
import pandas as pd

from datetime import datetime

class apiBase:

    def __init__(self, name, per_step, sleep):
        self.name = name
        self.per_step = per_step
        self.sleep = sleep

        self.default_columns = ['high', 'volume', 'low', 'close', 'open']
        self.symbol_dict = None
        self.start = None
        self.limit = None

        self.suppress_warning = False

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def interval_check(self, interval):
        if 'h' in interval:            
            interval = int(interval.split('h')[0]) * 3600
            minutes = int(interval / 60)    
        elif 'm' in interval:
            interval = int(interval.split('m')[0]) * 60
            minutes = int(interval / 60)            
        else:
            raise Exception('Only hours supportted right now')
        return interval, minutes

    def symbol_check(self, symbol):
        # symbol = 'btcusd' if symbol is None else symbol
        if symbol in self.symbol_dict:
            symbol = self.symbol_dict[symbol]
        else:
            if not self.suppress_warning:
                print('Warning: Not using a supported symbol, not every module might work.')
                self.suppress_warning = True
        return symbol

    def response_handler(self, address, params, timeout=60):
        r = requests.get(address, params=params, timeout=timeout)

        if r.status_code != 200:
            # if str(r.status_code).startswith('5'):
            #     r.raise_for_status()

            tries = 4
            retry_after = 10
            for i in range(tries):            
                if r.status_code == 429:
                    retry_after += int(r.headers['Retry-After'])

                print(f'\nResponse: {r.status_code} for {self.name}, trying after {retry_after}secs')
                try:
                    print(r.json())
                except:
                    pass
                # r.raise_for_status()
                time.sleep(retry_after)

                r = requests.get(address, params=params, timeout=timeout)
                if r.status_code == 200:
                    break
        else:
            return r

        r.raise_for_status()

    def get_hist(self,
            symbol = None,
            start = None, 
            end = None,
            columns = None,
            interval = '1h',    # Don't use this for now, only 1h is supported
            global_columns=True,
            interpolate=True,   # Should be ok to enable I guess, check later
            df_update=None,
            ):      

        # init
        verbose_after = 10     
        name = f'{self.name}_{interval}'
        columns = columns or self.default_columns
        start = start or self.start
        end = end or int(time.time())

        interval_str = interval     # to give it to .get() func
        interval, minutes = self.interval_check(interval)

        total_entries = (end - start) // interval
        steps = (total_entries // self.per_step) + 1

        df = pd.DataFrame(columns=columns)
        df.index.name = 'timestamp'

        if steps > verbose_after:
            print(f'Downloading {name}')
        
        for i in range(steps):
            start_batch = start + (interval*i*self.per_step)
            end_batch = start_batch + (interval*self.per_step)
            if end_batch >= end:
                end_batch = end
            try:
                df_temp = self.get(symbol=symbol, interval=interval_str, start=str(start_batch), end=str(end_batch))
                if df_temp is None:     # Try this fix for other apis
                    print('    Debug: df_temp is empty')
                    assert len(df) == 0, 'Debug: empty df_temp in middle of download'
                    df_temp = df
            except Exception as e:
                # raise e
                print(e, '\nDebug: error between timestamps: ', start_batch, end_batch)
                if steps <= 1: return None

            df_temp = pd.concat([df, df_temp])
            df = df_temp

            if steps > verbose_after:
                print('\r' + f'  {i} of {steps}', end='')
            time.sleep(self.sleep)

        if global_columns:
            df = df[columns]
        # df = df.drop_duplicates(subset='timestamp')
        df = df[~df.index.duplicated(keep='first')]        
        df = df.astype(float)       # check this one

        if df_update:   # check this later
            df = pd.concat([df_update, df])
            df = df[~df.index.duplicated(keep='first')]

        if interpolate:
            # interpolate nan data
            df.replace(0, np.nan, inplace=True)
            df.interpolate(inplace=True)
        
        # if steps > verbose_after:
        print(f'\n  Completed: {self.name}')

        # df['date'] = pd.to_datetime(df.index, unit='s', utc=True)
        
        return df

    def update(self, path, **kwargs):
        # assert os.path.exists(path), "path doesn't exists!"
        if not os.path.exists(path):    # Disabled
            assert '.csv' in path, "Not a valid .csv location!"
            print("Couldn't find a file to update, downloading all history now..")
            df = self.get_hist()
            df.to_csv(path)
            return
        
        df = pd.read_csv(path, index_col=0)

        last_timestamp = df.index[-1]
        updates = self.get_hist(start=last_timestamp, **kwargs)

        df_final = pd.concat([df, updates])
        df_final = df_final[~df_final.index.duplicated(keep='first')]
        df_final.to_csv(path)

        return df_final

    def calc_start(self, limit, start=None, end=None, interval=3600, scale=1):
        current_time = int(time.time())
        if isinstance(interval, str):
            interval = self.interval_check(interval)[0]

        limit = self.limit if limit is None else limit
        limit = int(limit / scale)      # for 8h funding scaling
        end = current_time if end is None else end
        if start is None:
            start = end - (interval * (limit-1))  # limit -1 to be sure to get the latest hour
        out_of_range = True if limit > self.limit else False
        return start, end, out_of_range
    
    def to_ts(self, df):   # Convert datetime to timestamp        
        return df.values.astype(np.int64) // 10 ** 9

    def to_date(self, x):       # Convert timestamp to datetime
        return pd.to_datetime(x, unit='s', utc=True)

    def ts_to_mts(self, time):
        # second timestamp to millisecond timestamp
        if time:
            if len(str(time)) == 10:
                return int(time)*1000
            else:
                assert len(str(time)) == 13, 'Please use a timestamp value with lenght 10!'
                return int(time)
