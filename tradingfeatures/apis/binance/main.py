import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.binance.base import binanceBase


# class binance():

#     def __init__(self):
        
#         self.base = binanceBase()

#     def get(self, *args, **kwargs):
#         return self.base.get(*args, **kwargs)

#     def get_hist(self, *args, **kwargs):
#         return self.base.get_hist(*args, **kwargs)

#     def update_all(self):
#         """
#             Update everything that api offers.
#         """
#         raise NotImplementedError

class binance(binanceBase):

    def __init__(self):
        super(binance, self).__init__()

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError