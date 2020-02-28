# bitfinexget
A small package to get history, easily download all avaliable history to csv or update current csv files


## Installation

    pip install git+https://github.com/realiti4/bitfinexget

## Example

To get current history(max 10000)

    from bitfinexget import bitfinex

    bitfinex = bitfinex()

    bitfinex.get(1000)

