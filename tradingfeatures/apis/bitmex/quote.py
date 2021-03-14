import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitmex.base import bitmexBase


class bitmexQuote(bitmexBase):

    def __init__(self):
        super(bitmexQuote, self).__init__()
        self.name = 'bitmex_quote'
        self.address = '/quote/bucketed'
        self.start = 1423227200        

    def get(self, symbol=None, query=None, start=None, end=None, *args, **kwargs):
        # start = self.start if start is None else start
        # end = time.time() if end is None else end
        # start, end = self.to_date(start), self.to_date(end)
        # symbol = symbol or 'XBT'
        
        # if query is None:
        #     query = {'symbol': symbol, 'binSize': interval, 'count': self.limit, 'reverse': 'false', 'startTime': start}

        return super(bitmexQuote, self).get(
            query=query,
            start=start,
            end=end,
            *args, **kwargs
        )

    def get_hist(self, start=1463227200, convert_funds=False, *args, **kwargs):
        df = apiBase.get_hist(
            self,
            columns=['bidSize', 'bidPrice', 'askPrice', 'askSize'],
            # interval='8h',
            *args, **kwargs
        )

        return df
