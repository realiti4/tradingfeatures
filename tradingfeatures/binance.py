import time
import requests
import pandas as pd

from datetime import datetime

from tradingfeatures import api_base

class binance(api_base):

    def __init__(self):
        super(binance, self).__init__(
            name = 'binance_1h',
            per_step = 1000,
            sleep = 0.7,
        )

    def get(self, start=1484778000, end=int(time.time())):
        start, end = (start*1000), (end*1000)
        currency_pair = 'BTCUSDT'
        add = '/api/v3/klines'
        address = 'https://api.binance.com' + add
        query = {'symbol': currency_pair, 'interval': '1h', 'startTime': start, 'endTime': end, 'limit': 1000}

        r = requests.get(address, params=query)

        result = r.json()

        df = pd.DataFrame(result, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                                    'number_of_trades', 'taker_base_asset_volume', 'taker_quote_asset_volume', 'ignore'])

        print('debug')
    
    
