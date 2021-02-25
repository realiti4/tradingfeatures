import time
import requests
import pandas as pd

from tradingfeatures import bitfinex
from tradingfeatures import bitmex


class base:

    def __init__(self):
        self.bitfinex = bitfinex()
        self.bitmex = bitmex()

        self.columns = ['close', 'low', 'high', 'volume', 'fundingRate']

    def get(self, limit=10000):
        df_bitfinex = self.bitfinex.get(10000)
        df_bitmex = self.bitmex.get_funding_rates(save_csv=False)

        merged = self.bitmex.price_funding_merger(df_bitfinex, df_bitmex)

        merged = merged[self.columns]

        return merged.to_numpy()

# base = base()

# test = base.get()

# test.to_csv('testtest.csv', index=False)