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

        # print('debug')

        # self.get_hist('1h',)

        # # Bitmex remaining limit
        # if 'x-ratelimit-remaining' in r.headers:
        #     if int(r.headers['x-ratelimit-remaining']) <= 1:
        #         print('sleeping...')
        #         time.sleep(61)
        return df

    def get_hist(self, timeframe, start=1364778000, end=int(time.time()), symbol='tBTCUSD'):
        # if timeframe not in self.times_dict:
        #     raise Exception('enter a valid timeframe')

        # minutes = self.times_dict[timeframe]
        minutes = 60
        interval = 60 * minutes
        per_step = 1000

        total_entries = (end - start) // interval
        steps = (total_entries // per_step) + 1
        # if steps == 0: steps = 1
        df = pd.DataFrame(columns=['high', 'timestamp', 'volume', 'low', 'close', 'open'])

        for i in range(steps):
            start_batch = start + (interval*i*per_step)
            end_batch = start_batch + (interval*per_step)
            try:
                df_temp = self.test(start=str(start_batch), end=str(end_batch))
            except:
                print('hata!', start_batch, end_batch)
                if steps <= 1: return None

            # print(len(df_temp))

            df_temp = pd.concat([df, df_temp])            
            df = df_temp

            print(f'  {i} of {steps}')
            # time.sleep(1.01)

        df.drop_duplicates(subset='timestamp', inplace=True)
        df = df.astype(float)
        
        # df['date'] = conv_time_v2(df['timestamp'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
        
        return df
    
    def get_funding_rates(self, df_path=None, reverse='false', save_csv=True):

        address = 'https://www.bitmex.com/api/v1/funding'
        symbol = 'XBT'
        query = {'symbol': symbol, 'count': 500, 'reverse': 'false', 'startTime': 0}        

        r = self.get_(address, query)

        appended_data = []

        # For updates
        if df_path:
            df_fundings = pd.read_csv(df_path)  # check if it is proper
            appended_data.append(df_fundings)

            last_time = df_fundings['timestamp'][-1:]
            query['startTime'] = last_time             

        for i in range(10000):
            r = self.get_(address, query)

            df_fundings = pd.read_json(r.content)

            appended_data.append(df_fundings)

            if len(df_fundings) < query['count']:
                print('completed!')
                break

            last_time = df_fundings['timestamp'][-1:]
            query['startTime'] = last_time 

        df_fundings = pd.concat(appended_data, ignore_index=True).drop_duplicates()
        if save_csv:
            df_fundings.to_csv('bitmex_fundings.csv', index=False)
        else:
            return df_fundings        

    def price_funding_merger(self, df, df_fundings):
        # TODO clean it, check it for things that might be missed

        df_fundings['date'] = pd.to_datetime(df_fundings['timestamp'])
        df['date'] = pd.to_datetime(df['date'])

        # a much better merger
        df.set_index('date', inplace=True)
        df_fundings.set_index('date', inplace=True)
        df_fundings.pop('timestamp')

        merged = df.join(df_fundings)
        merged.fillna(method='ffill', inplace=True)

        return merged

    def shorts_longs(self):
        # TODO
        pass

