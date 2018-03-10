import http.client,urllib.parse


class KrakenAPIHandle:
    def __init__(self):
        self.HOST = "api.kraken.com"

    def new_connection(self):
        return http.client.HTTPSConnection(self.HOST, port=http.client.HTTPS_PORT)

    def get_asset_pairs(self):
        conn = self.new_connection()
        conn.request('GET', '/0/public/AssetPairs')
        return self._read_response(conn.getresponse())

    def get_time(self):
        conn = self.new_connection()
        conn.request('GET','/0/public/Time')
        return self._read_response(conn.getresponse())

    def get_ticker(self, pairs):
        conn = self.new_connection()
        pair_string = self._set_to_string(pairs)
        param = urllib.parse.urlencode({'pair': pair_string})
        conn.request('POST', '/0/public/Ticker', param)

        return self._read_response(conn.getresponse())

    # raise HTTPException when response status is not 200
    def get_orderbook(self, pairs, count):
        conn = self.new_connection()
        pair_string = self._set_to_string(pairs)
        param = urllib.parse.urlencode({'pair': pair_string, 'count': count})

        conn.request('POST', '/0/public/Depth', param)

        return self._read_response(conn.getresponse())

    def _read_response(self, resp):
        if resp.status != 200:
            raise http.client.HTTPException("%s: %s" % (resp.reason, resp.status))
        return resp.read()

    def _set_to_string(self, pairs):
        param_string = ''
        count = 0
        for p in pairs:
            if count != 0:
                param_string += ","
            param_string += p
            count += 1

        return param_string
