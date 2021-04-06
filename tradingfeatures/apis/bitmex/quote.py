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
        self.start = 1442227200
        self.default_columns = ['bidSize', 'bidPrice', 'askPrice', 'askSize']

    def get(self, query=None, start=None, end=None, *args, **kwargs):

        return super(bitmexQuote, self).get(
            query=query,
            start=start,
            end=end,
            *args, **kwargs
        )

    def get_hist(self, symbol=None, convert_funds=False, *args, **kwargs):
        symbol = symbol or 'btcusd'
        self._start_check(self.address, symbol=symbol)
        # columns = ['bidSize', 'bidPrice', 'askPrice', 'askSize'] if columns is None else columns

        df = apiBase.get_hist(
            self,
            symbol=symbol,
            # columns=columns,
            # interval='8h',
            *args, **kwargs
        )

        return df
