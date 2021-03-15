# tradingfeatures
A useful tool to download market history from popular exchanges.


## Installation

    pip install tradingfeatures

or	

    pip install git+https://github.com/realiti4/tradingfeatures.git@master --upgrade

## Example
You can use `.get()`, `.get_history()` and `.update()` with all avaliable apis. Currently supported:

* Bitfinex
* Bitstamp
* Binance
* Bitmex

### Get history with .get()

    import pandas as pd
    from tradingfeatures import bitfinex, bitstamp, binance, bitmex

    bitfinex = bitfinex()

    df = bitfinex.get(2000)

Just pass how much data you want. It will return the amount in most recent 1h data. Currently only 1h data is supported. If history amount is above api limit, `.get()` will run `.get_history()` under the hood, so you don't need to worry about it. But if you want everything and don't want to guess how much data avaliable on each exchange, just run `.get_history()` and get everything.

### Download all available history with .get_history()
The tool will download all avaliable history while respecting request per minute limits. Using it easy, and it takes couple of minutes for 1h data.

    import pandas as pd
    from tradingfeatures import bitfinex, bitstamp, binance, bitmex

    bitstamp = bitstamp()
    
    df = bitstamp.get_hist()
    df.to_csv('bitstamp_1h.csv') 

### Updating a csv file with .update()

    import pandas as pd
    from tradingfeatures import bitfinex, bitstamp, binance, bitmex

    bitstamp = bitstamp()
    
    bitstamp.update_csv('bitstamp.csv')    

Update takes a path variable to csv file and updates it.
