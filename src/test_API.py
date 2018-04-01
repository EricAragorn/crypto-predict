import http.client
import json

from src.api_handle import APIHandle


def main():
    handle = APIHandle()
    try:
        print(json.dumps(handle.get_time(), indent=4, sort_keys=False))
        # print(json.dumps(json.loads(handle.get_orderbook({"XBTUSD"}, count=10).decode()), indent=4, sort_keys=True))
    except http.client.HTTPException as e:
        print("HTTP request failed: %s" % e.args)


if __name__ == "__main__":
    main()
