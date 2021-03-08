import time
import requests
import numpy as np
import pandas as pd


class bitmex:

    def get_(self, address, query):
        r = requests.get(address, params=query, timeout=60)
        if r.status_code != 200:    # Bad response handler
            print(r.json())
            r.raise_for_status()
        
        # Bitmex remaining limit
        if 'x-ratelimit-remaining' in r.headers:
            if int(r.headers['x-ratelimit-remaining']) <= 1:
                print('reached the rate limit, bitmex api is sleeping...')
                time.sleep(61)
        return r
    
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
        df_fundings['timestamp'] = df_fundings.timestamp.values.astype(np.int64) // 10 ** 9
        # df_fundings['date'] = pd.to_datetime(df_fundings['timestamp'], unit='s', utc=True)
        df_fundings.set_index('timestamp', inplace=True)
        if save_csv:
            df_fundings.to_csv('bitmex_fundings.csv', index=False)
        else:
            return df_fundings        

    def price_funding_merger(self, df, df_fundings):
        merged = df.join(df_fundings)
        merged.fillna(method='ffill', inplace=True)

        return merged

    def shorts_longs(self):
        # TODO
        pass


# trading_features().get_funding_rates()