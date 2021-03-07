# tradingfeatures
A useful tool to downlaod market history from popular exchanges.


## Installation

    pip install tradingfeatures

or	

    pip install git+https://github.com/realiti4/tradingfeatures.git@master --upgrade

## Example
You can use `.get()`, `.get_history()` and `.update()` with all avaliable apis. Currently supported:

* Bitfinex
* Bitstamp

### Get most recent history with .get()

    import pandas as pd
    from tradingfeatures import bitfinex, bitstamp

    bitfinex = bitfinex()

    df = bitfinex.get()

This is useful to get most recent history. But limit is 10000 for Bitfinex and 1000 for Bitstamp.

### Download all available history with .get_history()
The tool will download all avaliable history while respesting request per minute limits. Using it easy, and it takes couple of minutes for 1h data.

    import pandas as pd
    from tradingfeatures import bitfinex, bitstamp

    bitstamp = bitstamp()
    
    df = bitstamp.get_hist()
    df.to_csv('bitstamp_1h.csv') 

### Updating a csv file with .update()

    import pandas as pd
    from tradingfeatures import bitfinex, bitstamp

    bitstamp = bitstamp()
    
    bitstamp.update_csv('bitstamp.csv')    

Update takes a path variable to csv file and updates it.
