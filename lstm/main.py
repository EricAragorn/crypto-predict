from __future__ import division
from __future__ import absolute_import

import tensorflow as tf
import pandas as pd
import model


class ModelConfig:
    def __init__(self):
        # features used for prediction and targets
        self.feature_list = ["open", "high", "low", "close", "vwap", "volume", "count",
                             "ask price5", "ask volume5", "ask price4", "ask volume4",
                             "ask price3", "ask volume3", "ask price2", "ask volume2",
                             "ask price1", "ask volume1", "bid price1", "bid volume1",
                             "bid price2", "bid volume2", "bid price3", "bid volume3",
                             "bid price4", "bid volume4", "bid price5", "bid volume5"]

        self.target_list = ["high", "low"]
        self.feature_size = len(self.feature_list)
        self.target_size = len(self.target_list)

        # Run configurations
        self.batch_size = 20  # training batch size
        self.num_steps = 60  # number of records feed into LSTM
        self.time_lap = 1  # time lap between last record of input and target record
        self.training_ratio = 0.75  # ratio of training set to data set
        self.initial_lr = 0.05
        self.lr_decay_rate = 0.8
        self.max_epoches = 20
        self.decay_range = 10  # start weight decay after epoch exceeds range
        self.max_grad_norm = 10

        # LSTM settings
        self.hidden_size = self.feature_size  # hidden units of a single LSTM cell
        self.dropout_prob = 0.1  # dropout_
        self.num_layers = 5


class CryptoData:
    # TODO: Modify this class to initialize with pandas Dataframe instead of file path
    def __init__(self, path, model_config):
        raw_data = pd.read_csv(path).fillna(0)

        split_loc = int(len(raw_data) * 0.75)
        self._training_set = raw_data.iloc[:split_loc, :]
        self._validation_set = raw_data.iloc[split_loc + 1:, :]
        self._config = model_config

        # initialize batching state
        self._batch_base = 0
        self._finished = False

    def next_training_batch(self, batch_size, num_steps, time_lap):
        if self._finished is True: raise BaseException("No more batches")
        batchX, batchY = [], []
        training_set = self._training_set
        base = self._batch_base

        for index in range(batch_size):
            if base + index + num_steps + time_lap < len(training_set):
                batchX.append(training_set.iloc[base + index: base + index + num_steps, :][self._config.feature_list].values)
                batchY.append(training_set.iloc[base + index + num_steps + time_lap, :][self._config.target_list].values)
            else:
                self._finished = True
                break

        self._batch_base += batch_size
        return batchX, batchY

    # WARNING: It is an incomplete version of fetching validation data
    #          Currently it only fetches the first <batch_size> samples from the validation set
    #          Will be removed in the future
    def validation_set(self, batch_size):
        batchX, batchY = [], []
        steps = self._config.num_steps
        time_lap = self._config.time_lap
        v_set = self._validation_set
        for index in range(batch_size):
            batchX.append(v_set.iloc[0 + index: 0 + index + steps, :][self._config.feature_list].values)
            batchY.append(v_set.iloc[0 + index + steps + time_lap, :][self._config.target_list].values)

        return batchX, batchY

    def is_finished(self):
        return self._finished

    # Reset batching state
    def reset(self):
        self._batch_base = 0
        self._finished = False


def main(args):
    # TODO: Create an independent function for training & validation to improve readability
    # TODO: Fix gradient vanishing problem after a certain epochs
    model_config = ModelConfig()
    data = CryptoData(path="../data/market_data.csv", model_config=model_config)

    with tf.Graph().as_default(), tf.Session() as sess:
        m = model.LSTMModel(is_training=True, model_config=model_config)
        tf.global_variables_initializer().run()
        global_step = 0
        for epoch in range(model_config.max_epoches):
            lr_decay = model_config.lr_decay_rate ** max(epoch - model_config.decay_range, 0)
            sess.run(m.update_lr, feed_dict={m._new_lr: lr_decay * model_config.initial_lr})
            data.reset()

            train_loss = 0
            batch_count = 0
            while not data.is_finished():
                trainX, trainY = data.next_training_batch(batch_size=model_config.batch_size,
                                                          num_steps=model_config.num_steps,
                                                          time_lap=model_config.time_lap)
                if len(trainX) == model_config.batch_size:
                    _, _loss = sess.run([m.train_op, m.loss], feed_dict={m.input: trainX, m.target: trainY})
                    global_step += 1
                    train_loss += _loss
                    batch_count += 1
            valX, valY = data.validation_set(model_config.batch_size)
            val_loss = sess.run(m.loss, feed_dict={m.input: valX, m.target: valY})
            print("Epoch: {:d}, Global steps: {:d}\n  Training Loss: {:.1f}, Validation Loss: {:.1f}"
                  .format(epoch, global_step, train_loss / batch_count, val_loss))


if __name__ == "__main__":
    tf.app.run()
