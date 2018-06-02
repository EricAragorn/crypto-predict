import tensorflow as tf
import pandas as pd
import numpy as np


def main(args):
    market_data = pd.read_csv("../data/market_data.csv")
    print(market_data.info())

if __name__ == "__main__":
    tf.app.run()