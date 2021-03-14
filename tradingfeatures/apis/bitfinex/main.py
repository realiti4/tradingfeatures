import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitfinex.base import bitfinexBase


class bitfinex():

    def __init__(self):
        
        self.base = bitfinexBase()

    def get(self, *args, **kwargs):
        return self.base.get(*args, **kwargs)

    def get_hist(self, *args, **kwargs):
        return self.base.get_hist(*args, **kwargs)

    def update_all(self):
        """
            Update everything that api offers.
        """
        raise NotImplementedError
