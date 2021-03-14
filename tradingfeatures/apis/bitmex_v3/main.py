import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitmex_v3.base import bitmexBase
from tradingfeatures.apis.bitmex_v3.funding import bitmexFunding
from tradingfeatures.apis.bitmex_v3.quote import bitmexQuote


class bitmexV3():

    def __init__(self):
        
        self.base = bitmexBase()
        self.funding = bitmexFunding()
        self.quote = bitmexQuote()

        print('debug')

    def get(self, *args, **kwargs):
        return self.base.get(*args, **kwargs)

    def get_hist(self, *args, **kwargs):
        return self.base.get_hist(*args, **kwargs)

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError
