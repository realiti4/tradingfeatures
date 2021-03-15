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

        return super(bitmexQuote, self).get(
            query=query,
            start=start,
            end=end,
            *args, **kwargs
        )

    def get_hist(self, columns=None, convert_funds=False, *args, **kwargs):
        columns = ['bidSize', 'bidPrice', 'askPrice', 'askSize'] if columns is None else columns

        df = apiBase.get_hist(
            self,
            columns=columns,
            # interval='8h',
            *args, **kwargs
        )

        return df
