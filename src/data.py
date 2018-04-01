from enum import Enum, unique


@unique
class AssetPairs(Enum):
    XBTUSD = "XBTUSD"
    LTCUSD = "LTCUSD"
    XRPUSD = "XRPUSD"


class ExchangeMode(Enum):
    GDAX = "GDAX"
    KRAKEN = "KRAKEN"


class APILink:
    def __init__(self,
                 host,
                 assetpair,
                 time,
                 ticker,
                 ohlc,
                 orderbook):
        self.host = host
        self.assetpair = assetpair
        self.time = time
        self.ticker = ticker
        self.ohlc = ohlc
        self.orderbook = orderbook


class KrakenAPILink(APILink):
    def __init__(self):
        APILink.__init__(self,
                         host="api.kraken.com",
                         assetpair="/0/public/AssetPairs",
                         time="/0/public/Time",
                         ticker="/0/public/Ticker",
                         ohlc="/0/public/OHLC",
                         orderbook="/0/public/Depth")
