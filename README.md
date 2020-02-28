# bitfinexget
A small package to get history, easily download all avaliable history to csv or update current csv files


## Installation

    pip install bitfinexget

## Example

### To get current history(max 10000)

    from bitfinexget import bitfinex

    bitfinex = bitfinex()

    bitfinex.get(1000)

### Download history
Bitfinex limits latest history call to 10000. If you would like get older data it is more stricter. But you can specify a start and finish timestamp like below and get all 1h data under 5-10 minutes while respecting Bitfinex's api call limits.

    df = bitfinex.get_hist(['1h', 60])
    df.to_csv('data/bitfinex_1h_downloaded.csv', index=False)
    
    df = bitfinex.get_hist(['30m', 30], start=1464778000, end=int(time.time()))
    df.to_csv('data/tradingview/bitfinex_30m_downloaded.csv', index=False)

Select the gap (5m, 15m, 30m, 1h, 3h, 6h, 12h) etc. and don't remember to change minutes equivalent, like ['15m', 15], ['3h', 240]

By default it will try to download all avaliable history up to current date. You can also specify any timestamp with 'start=1464778000' and 'end=1564778000'


### Update csv file

    bitfinex.update_csv('data/bitfinex_1h_downloaded.csv', times_to_get=[['1h', 60]]
    bitfinex.update_csv('data/bitfinex_5m_downloaded.csv', times_to_get=[['5m', 5]]

