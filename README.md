# tradingfeatures
A useful tool to get market history and other features while respecting api limits.


## Installation

    pip install tradingfeatures

## Example

### To get current history(max 10000)

    from tradingfeatures import bitfinex

    bitfinex = bitfinex()

    bitfinex.get(1000)

### Download history
Bitfinex limits latest history call to 10000. If you would like get older data it is even more stricter. But you can specify a start and finish timestamp like below and get all 1h data under 5-10 minutes while respecting Bitfinex's api call limits. By default it'll download the entire history and you don't need to pass 'start' and 'end'

    df = bitfinex.get_hist('1h')
    df.to_csv('data/bitfinex_1h_downloaded.csv', index=False)
    
    df = bitfinex.get_hist('30m', start=1464778000, end=int(time.time()))
    df.to_csv('data/bitfinex_30m_downloaded.csv', index=False)


By default it will try to download all avaliable history up to current date. You can also specify any timestamp like 'start=1464778000' and 'end=1564778000'


### Update csv file

    bitfinex.update_csv('data/bitfinex_1h_downloaded.csv', timeframes=['1h']
    bitfinex.update_csv('data/bitfinex_5m_downloaded.csv', timeframes=['5m', '3h']

When updating you can pass multiple timeframes in a list to update all in once.
