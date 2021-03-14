import time
import requests
import numpy as np
import pandas as pd

from tradingfeatures import apiBase
from tradingfeatures.apis.bitmex.base import bitmexBase
from tradingfeatures.apis.bitmex.funding import bitmexFunding
from tradingfeatures.apis.bitmex.quote import bitmexQuote


class bitmex(bitmexBase):

    def __init__(self):
        super(bitmex, self).__init__()
        
        self.funding = bitmexFunding()
        self.quote = bitmexQuote()

    def update_all(self, folder_path='uber_data'):
        """
            Update everything that api offers.
        """
        assert '.csv' not in folder_path, 'Use a folder path'
        name_func = lambda x: f'{folder_path}/{x.name}.csv'

        self.funding.update(name_func(self.funding))
        self.quote.update(name_func(self.quote))

        print('Successful..')