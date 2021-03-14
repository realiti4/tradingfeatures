import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitstamp.base import bitstampBase



class bitstamp(bitstampBase):

    def __init__(self):
        super(bitstamp, self).__init__()

    def update(self, path, update_all=False, *args, **kwargs):        
        if update_all:
            return self.update_all(*args, **kwargs)
        else:
            return super(bitstamp, self).update(path, *args, **kwargs)

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError
