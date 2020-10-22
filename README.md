# tradingfeatures
A useful tool to get market history and other features while respecting api limits.


## Installation

    pip install tradingfeatures

## Example

### To get current history(max 10000)

    from tradingfeatures import bitfinex

    bitfinex = bitfinex()

    bitfinex.get(1000)

### Download all available history
Bitfinex limits most recent history call to 10000. If you would like get older data it is even more stricter. But you can download all history in 2 lines with this tool easily under 5-10 minutes while respecting Bitfinex's api call limits. 

    from tradingfeatures import bitfinex
    bitfinex = bitfinex()

    df = bitfinex.get_hist('1h')
    df.to_csv('bitfinex_1h.csv', index=False)
    
    df = bitfinex.get_hist('30m', start=1464778000, end=int(time.time()))
    df.to_csv('bitfinex_30m.csv', index=False)

By default it'll download the entire history and you don't need to pass 'start' and 'end'. But you can also specify any timestamp 'start=1464778000' and 'end=1564778000' etc. like above.

### Updating a csv file

    bitfinex.update_csv('bitfinex_1h.csv', timeframes=['1h']
    bitfinex.update_csv('bitfinex_5m.csv', timeframes=['5m', '3h']

When updating you can pass multiple timeframes in a list to update all in once.
