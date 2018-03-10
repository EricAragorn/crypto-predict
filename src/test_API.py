import http.client

from src import kraken_api_handle


def main():
    handle = kraken_api_handle.KrakenAPIHandle()
    try:
        # print(handle.get_asset_pairs())
        print(handle.get_ticker({"XBTUSD"}))
    except http.client.HTTPException as e:
        print("HTTP request failed: %s" % e.args)


if __name__ == "__main__":
    main()
