import http.client
import json

from crawler.api_handle import APIHandle


def main():
    handle = APIHandle()
    try:
        # print(json.dumps(handle.get_ticker({"XLTCXXBT"}), indent=4, sort_keys=False))
        print(json.dumps(handle.get_orderbook({"XBTUSD"}, count=10), indent=4, sort_keys=True))
    except http.client.HTTPException as e:
        print("HTTP request failed: %s" % e.args)


if __name__ == "__main__":
    main()
