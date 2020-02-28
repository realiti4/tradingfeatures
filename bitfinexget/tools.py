import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime
from time import sleep



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

    def get(self, limit=None, interval='1h', start=None, end=None, sort=-1, date=True, numpy_array=False):
        query = {'limit': limit, 'start': start, 'end': end, 'sort': sort}
        symbol = 'tBTCUSD'
        # symbol = 'tETHUSD'

        r = requests.get(f'https://api-pub.bitfinex.com/v2/candles/trade:{interval}:{symbol}/hist', params=query)
        # TODO 500 reponse handling
        if str(r.status_code).startswith('5'):
            r.raise_for_status()

        data = r.json()
        data.reverse()

        df = pd.DataFrame(data, columns=self.columns)
        if date:
            df['date'] = conv_time_v2(df['timestamp'])
        if numpy_array:
            return df['close'].to_numpy()
        return df
    
    def get_hist(self, start, end, time_list, interval=60):
        hour = time_list[0]
        interval = 60 * time_list[1] * 1000
        steps = ((end - start) // interval) // 120
        if steps == 0: steps = 1
        df = pd.DataFrame(columns=self.columns)

        for i in range(steps):
            start_batch = start + (interval*i*120)
            end_batch = start_batch + (interval*120)
            try:
                df_temp = self.get(interval=hour, start=str(start_batch), end=str(end_batch), date=False)
            except:
                print('hata!', start_batch, end_batch)
                if steps <= 1: return None

            print(len(df_temp))

            df_temp = pd.concat([df, df_temp])            
            df = df_temp

            print(f'  {i} of {steps}')
            sleep(1.01)

        df['date'] = conv_time_v2(df['timestamp'])
        return df
    
    def update_csv(self, path, times_to_get=[['1h', 60]], alternative_mode=False):
        for times in times_to_get:
            csv_file = pd.read_csv(path, index_col=0)
            path_main, path_file = path.rsplit('/', 1)
            csv_file.to_csv(path_main+'/backup/'+path_file)

            # if not 'date' in csv_file:
            #     csv_file['date'] = conv_time_v2(csv_file['timestamp'].astype('int64'))

            last_time = csv_file.index[-1]
            current_time = int(time.time())*1000

            if alternative_mode:
                df = self.get(10000, interval=times[0])
                for i in range(len(df)):
                    if df['timestamp'][i] == last_time:
                        df = df[i+1:]                  
                        break
            else:
                df = self.get_hist(int(last_time), current_time, times)
            if df is None:
                print(f'{times[0]} is already up to date!')
                break     
            df.set_index('timestamp', inplace=True)

            frames = [csv_file, df]
            csv_file = pd.concat(frames)

            # Local-dev        
            csv_file.to_csv(path)
            print('updated...')

