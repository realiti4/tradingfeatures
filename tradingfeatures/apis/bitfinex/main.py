import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitfinex.base import bitfinexBase
from tradingfeatures.apis.bitfinex.shortlong import bitfinexShortLong


class bitfinex(bitfinexBase):

    def __init__(self):
        super(bitfinex, self).__init__()

        self.shortlong = bitfinexShortLong()

    def update(self, path, update_all=False, *args, **kwargs):        
        if update_all:
            return self.update_all(*args, **kwargs)
        else:
            return super(bitfinex, self).update(path, *args, **kwargs)

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError
