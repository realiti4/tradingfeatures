import time
import datetime

import pytrends
import numpy as np
import pandas as pd

from pytrends.request import TrendReq


class google_trends:
    def __init__(self, kw_list=['bitcoin']):

        self.pytrends = TrendReq()

        self.kw_list = kw_list

    def get(self, date_start, date_end=None, sleep=60):
        if date_end is None:
            date_end = datetime.datetime.utcfromtimestamp(self.current_time())

        date_start = date_start - datetime.timedelta(hours=4, minutes=0)
        date_end = date_end + datetime.timedelta(hours=4, minutes=0)
        
        df_temp = self.pytrends.get_historical_interest(
            self.kw_list, 
            year_start=date_start.year, month_start=date_start.month, day_start=date_start.day, hour_start=date_start.hour, 
            year_end=date_end.year, month_end=date_end.month, day_end=date_end.day, hour_end=date_end.hour, 
            cat=0, geo='', gprop='', sleep=sleep)

        return df_temp

    def update(self, path, save=False):
        path = path + '/trends_data.csv'

        df = pd.read_csv(path, index_col=0)

        if not self.current_time() - df.index[-1] >= 3600:
            return df

        date_start = datetime.datetime.utcfromtimestamp(df.index[-1])

        df_temp = self.get(date_start)

        df_temp.index = df_temp.index.astype(np.int64) // 10 ** 9     # Convert date to timestamp
        df_temp.pop('isPartial')
        df_temp.columns = ['google_trends']

        # temp check
        df_temp_hour = datetime.datetime.utcfromtimestamp(df_temp.index[-1]).hour
        current_hour = datetime.datetime.utcfromtimestamp(self.current_time()).hour

        if not df_temp_hour == current_hour:            
            with open("google_trends_log.txt", "a") as log_file:
                log_file.write(f"Warning couldn't get google trends data! Time: {datetime.datetime.now()}\n")
        
        df = pd.concat([df, df_temp])
        df = df[~df.index.duplicated(keep='first')]
        
        # Save
        if save:
            df.to_csv(path)

        return df       

    def current_time(self):
        return int((time.time() // 3600) * 3600)

