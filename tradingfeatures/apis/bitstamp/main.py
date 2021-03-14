import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitstamp.base import bitstampBase


# class bitstamp():

#     def __init__(self):
        
#         self.base = bitstampBase()

#     def get(self, *args, **kwargs):
#         return self.base.get(*args, **kwargs)

#     def get_hist(self, *args, **kwargs):
#         return self.base.get_hist(*args, **kwargs)

#     def update_all(self):
#         """
#             Update everything that api offers.
#         """
#         raise NotImplementedError

class bitstamp(bitstampBase):

    def __init__(self):
        super(bitstamp, self).__init__()

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError
