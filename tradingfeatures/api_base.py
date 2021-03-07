import time
import requests
import pandas as pd

from datetime import datetime

class apiBase:

    def __init__(self, name, per_step, sleep):
        self.name = name
        self.per_step = per_step
        self.sleep = sleep

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def response_handler(self, address, params, timeout=60):
        r = requests.get(address, params=params, timeout=timeout)

        if r.status_code != 200:
            if str(r.status_code).startswith('5'):
                r.raise_for_status()

            tries = 4
            retry_after = 10
            for i in range(tries):            
                if r.status_code == 429:
                    retry_after += int(r.headers['Retry-After'])

                print(f'\nResponse: {r.status_code}, trying after {retry_after}secs')
                time.sleep(retry_after)

                r = requests.get(address, params=params, timeout=timeout)
                if r.status_code == 200:
                    break
        else:
            return r

        r.raise_for_status()

    def get_hist(self, start=1364778000, end=int(time.time()), interval='1h'):
        # if timeframe not in self.times_dict:
        #     raise Exception('enter a valid timeframe')

        # minutes = self.times_dict[timeframe]
        minutes = 60
        interval = 60 * minutes        

        total_entries = (end - start) // interval
        steps = (total_entries // self.per_step) + 1

        df = pd.DataFrame(columns=['high', 'timestamp', 'volume', 'low', 'close', 'open'])

        print(f'  Downloading {self.name}')

        for i in range(steps):
            start_batch = start + (interval*i*self.per_step)
            end_batch = start_batch + (interval*self.per_step)
            try:
                df_temp = self.get(start=str(start_batch), end=str(end_batch))
            except Exception as e:
                print(e)
                print('hata!', start_batch, end_batch)
                if steps <= 1: return None

            df_temp = pd.concat([df, df_temp])            
            df = df_temp

            print('\r' + f'  {i} of {steps}', end='')
            # print(f'  {i} of {steps}')
            time.sleep(self.sleep)

        df.drop_duplicates(subset='timestamp', inplace=True)

        df = df.set_index('timestamp')
        df.index = df.index.astype(int)
        df = df.astype(float)
        
        # df['date'] = pd.to_datetime(df.index, unit='s', utc=True)
        
        return df

    def update(self, path=None):
        df = pd.read_csv(path, index_col='timestamp')

        last_timestamp = df.index[-1]

        updates = self.get_hist(start=last_timestamp)

        df_final = pd.concat([df, updates])

        df_final = df_final[~df_final.index.duplicated(keep='first')]

        df_final.to_csv(path)
