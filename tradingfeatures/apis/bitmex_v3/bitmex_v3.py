import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitmex_v3.price import bitmexPrice
from tradingfeatures.apis.bitmex_v3.fundings import bitmexFundings


class bitmexV3():

    def __init__(self):
        
        self.price = bitmexPrice()
        self.fundings = bitmexFundings()

        print('debug')

    def get(self, *args, **kwargs):
        return self.price.get(*args, **kwargs)

    def get_hist(self, *args, **kwargs):
        return self.price.get_hist(*args, **kwargs)
