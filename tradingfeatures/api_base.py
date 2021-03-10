import time
import requests
import numpy as np
import pandas as pd

from datetime import datetime

class apiBase:

    def __init__(self, name, per_step, sleep):
        self.name = name
        self.per_step = per_step
        self.sleep = sleep

        self.default_columns = ['high', 'timestamp', 'volume', 'low', 'close', 'open']

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def interval_check(self, interval):
        if 'h' in interval:            
            interval = int(interval.split('h')[0]) * 3600
            minutes = int(interval / 60)
            return interval, minutes
        else:
            raise Exception('Only hours supportted right now')

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

                print(f'\nResponse: {r.status_code}, trying after {retry_after}secs')
                print(r.json())
                # r.raise_for_status()
                time.sleep(retry_after)

                r = requests.get(address, params=params, timeout=timeout)
                if r.status_code == 200:
                    break
        else:
            return r

        r.raise_for_status()

    def get_hist(self,
            get = None,      # Takes a get function                     
            start = None, 
            end = None,
            name = None,
            columns = None,
            interval = '1h',
            global_columns=True,
            ):      

        # init        
        get = get or self.get
        name = f'{name}_{interval}'
        columns = columns or self.default_columns
        start = start or 1364778000
        end = end or int(time.time())

        interval, minutes = self.interval_check(interval)

        total_entries = (end - start) // interval
        steps = (total_entries // self.per_step) + 1

        df = pd.DataFrame(columns=columns)

        print(f'  Downloading {name}')
        
        for i in range(steps):
            start_batch = start + (interval*i*self.per_step)
            end_batch = start_batch + (interval*self.per_step)
            if end_batch >= end:
                end_batch = end
            try:
                df_temp = get(start=str(start_batch), end=str(end_batch))
            except Exception as e:
                print(e)
                print('error between timestamps: ', start_batch, end_batch)
                if steps <= 1: return None

            df_temp = pd.concat([df, df_temp])
            df = df_temp

            print('\r' + f'  {i} of {steps}', end='')
            # print(f'  {i} of {steps}')
            time.sleep(self.sleep)

        if global_columns:
            df = df[columns]
        df = df.drop_duplicates(subset='timestamp')

        df = df.set_index('timestamp')
        df.index = df.index.astype(int)
        df = df.astype(float)
        
        print(f'\nCompleted: {self.name}')
        # df['date'] = pd.to_datetime(df.index, unit='s', utc=True)
        
        return df

    def update(self, path=None):
        df = pd.read_csv(path, index_col='timestamp')

        last_timestamp = df.index[-1]

        updates = self.get_hist(start=last_timestamp)

        df_final = pd.concat([df, updates])

        df_final = df_final[~df_final.index.duplicated(keep='first')]

        df_final.to_csv(path)
        return df_final

    def to_ts(self, df):   # Convert datetime to timestamp        
        return df.values.astype(np.int64) // 10 ** 9

    def to_date(self, x):       # Convert timestamp to datetime
        return pd.to_datetime(x, unit='s', utc=True)
