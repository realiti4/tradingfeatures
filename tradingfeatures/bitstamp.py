import time
import requests
import pandas as pd

from datetime import datetime

class bitstamp:

    def test(self, start=1364778000, end=time.time()):
        currency_pair = 'btcusd'
        address = f'https://www.bitstamp.net/api/v2/ohlc/{currency_pair}/'
        # query = {'start': , 'end': , 'step': 3600, 'limit': 1000}
        query = {'start': start, 'end': end, 'step': 3600, 'limit': 1000}

        return self.get_(address, query)

    def get_(self, address, query):
        r = requests.get(address, params=query)
        if r.status_code != 200:    # Bad response handler
            print(r.json())
            r.raise_for_status()
        
        result = r.json()['data']['ohlc']

        df = pd.DataFrame(result)   # fix index
        # df['date'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
        # datetime.utcfromtimestamp(1364778000)

        return df

    def get_hist(self, timestamp='1h', start=1364778000, end=int(time.time()), symbol='tBTCUSD'):
        # if timeframe not in self.times_dict:
        #     raise Exception('enter a valid timeframe')

        # minutes = self.times_dict[timeframe]
        minutes = 60
        interval = 60 * minutes
        per_step = 1000

        total_entries = (end - start) // interval
        steps = (total_entries // per_step) + 1

        df = pd.DataFrame(columns=['high', 'timestamp', 'volume', 'low', 'close', 'open'])

        for i in range(steps):
            start_batch = start + (interval*i*per_step)
            end_batch = start_batch + (interval*per_step)
            try:
                df_temp = self.test(start=str(start_batch), end=str(end_batch))
            except:
                print('hata!', start_batch, end_batch)
                if steps <= 1: return None

            df_temp = pd.concat([df, df_temp])            
            df = df_temp

            print(f'  {i} of {steps}')
            # time.sleep(1.01)

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
