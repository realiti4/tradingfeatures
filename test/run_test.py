import pytest
from tradingfeatures import binance, bitmex, bitfinex, bitstamp, Uber

binance = binance()
bitmex = bitmex()
bitfinex = bitfinex()
bitstamp = bitstamp()
uber = Uber()

    
def test_get():
    df_binance = binance.get()
    df_bitmex = bitmex.get()
    df_bitfinex = bitfinex.get()
    df_bitstamp = bitstamp.get()

    assert df_binance.columns.to_list() == ['open', 'high', 'low', 'close', 'volume', 
                                        'quote_asset_vol', 'number_of_trades', 'taker_base_asset_vol', 
                                        'taker_quote_asset_vol', 'taker_sell_base_asset_vol']
    assert df_bitmex.columns.to_list() == ['open', 'high', 'low', 'close', 'trades', 'volume', 'vwap', 
                                        'lastSize', 'turnover', 'homeNotional', 'foreignNotional']
    assert df_bitfinex.columns.to_list() == ['open', 'close', 'high', 'low', 'volume']
    assert df_bitstamp.columns.to_list() == ['high', 'volume', 'low', 'close', 'open']

def test_get_get_hist():
    df_binance = binance.get(2000)
    df_bitmex = bitmex.get(2000)
    df_bitfinex = bitfinex.get(2000)
    df_bitstamp = bitstamp.get(2000)

def test_interval_get():
    df_binance = binance.get(interval='1m')
    df_bitmex = bitmex.get(interval='1m')
    df_bitfinex = bitfinex.get(interval='1m')
    df_bitstamp = bitstamp.get(interval='1m')

def test_funding():
    # Bitmex
    bitmex.funding.get()
    bitmex.funding.get(5000)
    bitmex.funding.get_hist()

    # Binance
    binance.funding.get()
    binance.funding.get(5000)
    binance.funding.get_hist()

def test_uber():
    df_eval = uber.eval_get(2000)
