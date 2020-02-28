# bitfinexget
A small package to get history, easily download all avaliable history to csv or update current csv files


## Installation

    pip install git+https://github.com/realiti4/bitfinexget

## Example

To get current history(max 10000)

    from bitfinexget import bitfinex

    bitfinex = bitfinex()

    bitfinex.get(1000)

Download history

    df = bitfinex().get_hist(1364778000000, int(time.time())*1000, ['1h', 60])
    df.to_csv('data/bitfinex_1h_downloaded.csv', index=False)
    
    df = bitfinex().get_hist(1364778000000, int(time.time())*1000, ['30m', 30])
    df.to_csv('data/tradingview/bitfinex_30m_downloaded.csv', index=False)
    
'1364778000000' is the starting timestamp. From my experience it is very close to what bitfinex has as the oldest. You can try to fine tune or select a more recent time. int(time.time())*1000 is the current timestamp. Select the gap (15m, 30m, 1h, 3h, 6h) etc. and don't remember to add minutes equivalent, like ['15m', 15]

Update csv file

    bitfinex().update_csv('data/bitfinex_1h_downloaded.csv', times_to_get=[['1h', 60]]
    bitfinex().update_csv('data/bitfinex_5m_downloaded.csv', times_to_get=[['5m', 5]]

