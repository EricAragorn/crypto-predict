import os
import csv
import time

from crawler import util
from crawler import config
from crawler.data import AssetPairs
from crawler.data import CSV_FILE_PATH
from crawler.api_handle import APIHandle

def start():
    with open(CSV_FILE_PATH, mode='a', newline='') as datafile:
        csv_writer = csv.writer(datafile, dialect='excel')

        if os.path.getsize(CSV_FILE_PATH) == 0:
            fieldnames = ["assetpair", "timestamp", "open", "high", "low", "close",
                          "vwap", "volume", "count"]
            for i in range(0, config.DEPTH_LEVEL):
                index = config.DEPTH_LEVEL - i
                fieldnames += ["ask price%d" % index, "ask volume%d" % index, "ask timestamp%d" % index]
            for i in range(0, config.DEPTH_LEVEL):
                index = i + 1
                fieldnames += ["bid price%d" % index, "bid volume%d" % index, "bid timestamp%d" % index]
            csv_writer.writerow(fieldnames)

        print("Writing to file %s..." % CSV_FILE_PATH)

        while True:
            try:
                fvect = feature_vector_builder(AssetPairs.XBTUSD.value)
                print(fvect)
                csv_writer.writerow(fvect)
                datafile.flush()
                time.sleep(config.TIME_LAPSE)
            except KeyboardInterrupt:
                return


def feature_vector_builder(assetpair):
    if assetpair is None:
        raise RuntimeError("Error in feature_vector_builder(): assetpair cannot be None")
    handle = APIHandle('kraken')
    vect = [assetpair]

    # add ohlc features to feature vector
    server_time = handle.get_time()["unixtime"]
    ohlc = handle.get_ohlc(pair=assetpair, interval=5, since=server_time - config.TIME_LAPSE)["%s" % assetpair][0]
    vect += (ohlc)

    depth = handle.get_orderbook({assetpair})["%s" % assetpair]
    for i in range(len(depth["asks"]) - 1, 0, -1):
        vect += (depth["asks"][i])
    for i in range(0, len(depth["bids"]), 1):
        vect += (depth["bids"][i])
    return vect

if __name__ == "__main__":
    start()