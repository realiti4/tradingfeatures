import time
import requests
import pandas as pd


class trading_features:

    def get_(self, address, query):
        r = requests.get(address, params=query)
        if r.status_code != 200:    # Bad response handler
            print(r.json())
            r.raise_for_status()
        
        # Bitmex remaining limit
        if 'x-ratelimit-remaining' in r.headers:
            if int(r.headers['x-ratelimit-remaining']) <= 1:
                print('sleeping...')
                time.sleep(61)
        return r
    
    def get_funding_rates(self):

        address = 'https://www.bitmex.com/api/v1/funding'
        symbol = 'XBT'
        query = {'symbol': symbol, 'count': 500, 'reverse': 'false', 'startTime': 0}        

        r = self.get_(address, query)

        appended_data = []

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
        df_fundings.to_csv('bitmex_fundings.csv')


    def shorts_longs(self):
        # TODO
        pass


# trading_features().get_funding_rates()