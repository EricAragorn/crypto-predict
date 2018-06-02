import http.client,urllib.parse
import json

from data import KrakenAPILink
import util


class APIHandle:

    def __init__(self, exchange_mode='kraken'):
        if exchange_mode == 'kraken':
            self.api_link = KrakenAPILink()
        else:
            raise NotImplementedError

    def new_connection(self):
        """Establish a new connection to api host

        Returns:
            A HTTPSConnection to self.api_link.host
        """
        return http.client.HTTPSConnection(self.api_link.host, port=http.client.HTTPS_PORT)

    def get_asset_pairs(self):
        """Get information of all asset pairs available on Kraken exchange

        Returns:
            A dictionary containing all asset pair information

            See https://www.kraken.com/help/api#get-asset-info for documentation

        Raises:
            RuntimeError: An error occurs when failed to retrieve server information
        """
        conn = self.new_connection()
        conn.request('GET', self.api_link.assetpair)
        resp = json.loads(self._read_response(conn.getresponse()).decode())
        if len(resp["error"]) != 0:
            raise RuntimeError("KrakenAPIHandle.get_asset_pairs(): %s" % util.list_to_string(resp["error"]))
        return resp["result"]

    def get_time(self):
        """Get Kraken server time

        Returns:
            A dictionary containing server time

            See https://www.kraken.com/help/api#get-server-time for documentation

        Raises:
            RuntimeError: An error occurs when failed to retrieve server information
        """
        conn = self.new_connection()
        conn.request('GET',self.api_link.time)
        resp = json.loads(self._read_response(conn.getresponse()).decode())
        if len(resp["error"]) != 0:
            raise RuntimeError("KrakenAPIHandle.get_time(): %s" % util.list_to_string(resp["error"]))
        return resp["result"]

    def get_ticker(self, pairs):
        """Get ticker infomation

            Args:
                pairs: a string containing asset pairs delimited by ","

            Returns:
                A dictionary containing ticker information

                See https://www.kraken.com/help/api#get-ticker-info for documentation

            Raises:
                RuntimeError: An error occurs when failed to retrieve server information
        """
        if pairs is None:
            raise Exception("KrakenAPIHandle.get_ticker() failed: pairs cannot be None")
        conn = self.new_connection()
        pair_string = util.list_to_string(pairs)
        param = urllib.parse.urlencode({'pair': pair_string})
        conn.request('POST', self.api_link.ticker, param)

        resp = json.loads(self._read_response(conn.getresponse()).decode())
        if len(resp["error"]) != 0:
            raise RuntimeError("KrakenAPIHandle.get_ticker(): %s" % util.list_to_string(resp["error"]))
        return resp["result"]

    def get_ohlc(self, pair, interval=1, since=None):
        """Get ticker infomation

            Args:
                pair: an asset pair string
                interval: the time interval of ohlc
                        (Available values: 1 (default), 5, 15, 30, 60, 240, 1440, 10080, 21600)
                since: return committed OHLC data since given id

            Returns:
                A dictionary containing ticker information

                See https://www.kraken.com/help/api#get-ticker-info for documentation

            Raises:
                RuntimeError: An error occurs when failed to retrieve server information
        """
        if pair is None:
            return
        conn = self.new_connection()
        if since is None:
            param = urllib.parse.urlencode({'pair': pair, 'interval': interval})
        else:
            param = urllib.parse.urlencode({'pair': pair, 'interval': interval, 'since': since})
        conn.request('POST', self.api_link.ohlc, param)

        resp = json.loads(self._read_response(conn.getresponse()).decode())
        if len(resp["error"]) != 0:
            raise RuntimeError("KrakenAPIHandle.get_ohlc(): %s" % util.list_to_string(resp["error"]))
        return resp["result"]

    # raise HTTPException when response status is not 200
    def get_orderbook(self, pairs, count=10):
        if pairs is None:
            return
        conn = self.new_connection()
        pair_string = util.list_to_string(pairs)
        param = urllib.parse.urlencode({'pair': pair_string, 'count': count})

        conn.request('POST', self.api_link.orderbook, param)

        resp = json.loads(self._read_response(conn.getresponse()).decode())
        if len(resp["error"]) != 0:
            raise RuntimeError("KrakenAPIHandle.get_orderbook(): Unable to retrieve orderbook")
        return resp["result"]

    def _read_response(self, resp):
        if resp.status != 200:
            raise http.client.HTTPException("%s: %s" % (resp.reason, resp.status))
        return resp.read()
