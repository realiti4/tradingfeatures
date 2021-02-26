import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime
from time import sleep

from pathlib import Path

"""
    version 0.3.0
    -timestamp conversion is changed to general UTC, TODO check if get_hist or update has any problems with it
"""

def conv_time_v2(time):
    time_list = time.tolist()
    if len(str(time_list[0])) == 13:
        time_list = [x/1000 for x in time_list]
        # print('timestamp divided..')

    x = map(datetime.fromtimestamp, time_list)
    x = list(x)
    return x

def column_order(df, order):
    df = df[[df.columns[i] for i in order]]
    return df

class bitfinex:
    def __init__(self):
        self.columns = ['timestamp', 'open', 'low', 'high', 'close', 'volume']

        self.times_dict = {'5m': 5, '15m': 15, '30m': 30, '1h': 60, '3h': 180, '6h': 360, '12h': 720}

    def get(self, limit=None, timeframe='1h', start=None, end=None, symbol='tBTCUSD', sort=-1, date=True, numpy_array=False):
        start, end = self.timestamp_mts(start), self.timestamp_mts(end)
        query = {'limit': limit, 'start': start, 'end': end, 'sort': sort}
        # symbol = 'tBTCUSD'
        # symbol = 'tETHUSD'

        r = requests.get(f'https://api-pub.bitfinex.com/v2/candles/trade:{timeframe}:{symbol}/hist', params=query)
        # TODO 500 reponse handling
        if str(r.status_code).startswith('5'):
            r.raise_for_status()

        data = r.json()
        data.reverse()

        df = pd.DataFrame(data, columns=self.columns)
        df['timestamp'] = df['timestamp'].div(1000).astype('int64')     # Fixing timestamp inside self.get

        if date:
            # df['date'] = conv_time_v2(df['timestamp'])
            df['date'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
        if numpy_array:
            return df['close'].to_numpy()
        return df
    
    def get_hist(self, timeframe, start=1364778000, end=int(time.time()), symbol='tBTCUSD'):
        if timeframe not in self.times_dict:
            raise Exception('enter a valid timeframe')

        minutes = self.times_dict[timeframe]

        interval = 60 * minutes
        steps = ((end - start) // interval) // 120
        # steps = steps + 1
        if steps == 0: steps = 1
        df = pd.DataFrame(columns=self.columns)

        for i in range(steps):
            start_batch = start + (interval*i*120)
            end_batch = start_batch + (interval*120)
            try:
                df_temp = self.get(timeframe=timeframe, start=str(start_batch), end=str(end_batch), date=False, symbol=symbol)
            except:
                print('hata!', start_batch, end_batch)
                if steps <= 1: return None

            print(len(df_temp))

            df_temp = pd.concat([df, df_temp])            
            df = df_temp

            print(f'  {i} of {steps}')
            sleep(1.01)

        # df['date'] = conv_time_v2(df['timestamp'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
        return df
    
    def update_csv(self, path, timeframes=['1h'], alternative_mode=False, symbol='tBTCUSD'):
        # TODO fix time_toget for update_csv as well
        for times in timeframes:
            if '/' not in path:
                path = './' + path

            csv_file = pd.read_csv(path, index_col=0)
            path_main, path_file = path.rsplit('/', 1)

            # save backup
            Path(path_main+'/backup').mkdir(parents=False, exist_ok=True)
            csv_file.to_csv(path_main+'/backup/'+path_file)

            # if not 'date' in csv_file:
            #     csv_file['date'] = conv_time_v2(csv_file['timestamp'].astype('int64'))

            last_time = csv_file.index[-1]
            current_time = int(time.time())

            if alternative_mode:
                df = self.get(10000, timeframe=times, symbol=symbol)
                for i in range(len(df)):
                    if df['timestamp'][i] == last_time:
                        df = df[i+1:]                  
                        break
            else:
                df = self.get_hist(times, start=int(last_time), end=current_time)
            if df is None:
                print(f'{times} is already up to date!')
                break     
            df.set_index('timestamp', inplace=True)

            frames = [csv_file, df]
            csv_file = pd.concat(frames)

            # Local-dev        
            csv_file.to_csv(path)
            print('updated...')

    def timestamp_mts(self, time):
        # second timestamp to millisecond timestamp
        if time:
            if len(str(time)) == 10:
                return int(time)*1000
            else:
                assert len(str(time)) == 13, 'Please use a timestamp value with lenght 10!'
                return int(time)
