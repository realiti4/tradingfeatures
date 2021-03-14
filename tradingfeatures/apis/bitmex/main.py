import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitmex.base import bitmexBase
from tradingfeatures.apis.bitmex.funding import bitmexFunding
from tradingfeatures.apis.bitmex.quote import bitmexQuote


# class bitmex():

#     def __init__(self):
        
#         self.base = bitmexBase()
#         self.funding = bitmexFunding()
#         self.quote = bitmexQuote()

#         self.name = self.base.name

#     def get(self, *args, **kwargs):
#         return self.base.get(*args, **kwargs)

#     def get_hist(self, *args, **kwargs):
#         return self.base.get_hist(*args, **kwargs)

#     def update_all(self):
#         """
#             Update everything that api offers.
#         """
#         raise NotImplementedError

class bitmex(bitmexBase):

    def __init__(self):
        super(bitmex, self).__init__()
        
        self.funding = bitmexFunding()

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError    
