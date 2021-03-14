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
        self.start = 1463227200        

    def get(self, symbol=None, query=None, start=None, *args, **kwargs):
        return super(bitmexQuote, self).get(
            *args, **kwargs
        )

    def get_hist(self, start=1463227200, convert_funds=False, *args, **kwargs):
        df = apiBase.get_hist(
            self,
            columns=['timestamp', 'fundingRate', 'fundingRateDaily'],
            # interval='8h',
            *args, **kwargs
        )

        return df
