import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.binance.base import binanceBase
from tradingfeatures.apis.binance.funding import binanceFunding
from tradingfeatures.apis.binance.order_book import binanceOrderBook


class binance(binanceBase):

    def __init__(self):
        super(binance, self).__init__()

        self.funding = binanceFunding()
        self.orderbook = binanceOrderBook()

    def update(self, path, update_all=False, *args, **kwargs):        
        if update_all:
            return self.update_all(*args, **kwargs)
        else:
            return super(binance, self).update(path, *args, **kwargs)

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError