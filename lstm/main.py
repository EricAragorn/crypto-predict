import tensorflow as tf
import pandas as pd
import numpy as np
import config
import model


class Market_Data:
    def __init__(self):
        # Read data from file
        raw_data = pd.read_csv("../data/market_data.csv").fillna(0)

        # Shuffle and create training/validation set
        split_loc = int(len(raw_data) * 0.75)
        self._training_set = raw_data.iloc[:split_loc, :]
        self._validation_set = raw_data.iloc[split_loc + 1:, :]

        # initialize batching state
        self._batch_base = 0
        self._finished = False

    def next_training_batch(self, batch_size):
        if self._finished is True: raise BaseException("No more batches")
        batchX, batchY = [], []
        time_lap = config.time_lap
        training_set = self._training_set
        steps = config.num_steps
        base = self._batch_base

        for index in range(batch_size):
            if base + index + steps + time_lap < len(training_set):
                batchX.append(training_set.iloc[base + index: base + index + steps, :][config.feature_list].values)
                batchY.append(training_set.iloc[base + index + steps + time_lap, :][config.target_list].values)
            else:
                self._finished = True
                break

        self._batch_base += batch_size
        return batchX, batchY

    def validation_set(self, batch_size):
        batchX, batchY = [], []
        steps = config.num_steps
        time_lap = config.time_lap
        v_set = self._validation_set
        for index in range(batch_size):
            batchX.append(v_set.iloc[0 + index: 0 + index + steps, :][config.feature_list].values)
            batchY.append(v_set.iloc[0 + index + steps + time_lap, :][config.target_list].values)

        return batchX, batchY

    def is_finished(self):
        return self._finished

    # def small_batch(self):
    #     X = np.reshape(self._training_set.iloc[:config.num_steps, :][config.feature_list].values, [1, config.num_steps, config.feature_size])
    #     Y = np.reshape(self._training_set.iloc[config.num_steps + config.time_lap, :][config.target_list].values, [1, config.target_size])
    #     return X, Y

    # Reset batching state
    def reset(self):
        self._batch_base = 0
        self._finished = False

# def run_epoch(sess, model, config)


def main(args):
    data = Market_Data()

    with tf.Graph().as_default(), tf.Session() as sess:
        m = model.LSTMModel(is_training=True)
        tf.global_variables_initializer().run()
        global_step = 0
        for epoch in range(config.max_epoches):
            data.reset()
            while data.is_finished() is False:
                trainX, trainY = data.next_training_batch(config.batch_size)
                if len(trainX) == config.batch_size:
                    sess.run([m.train_op], feed_dict={m.input: trainX, m.target: trainY})
                    global_step += 1
                    print("Global Step:", global_step)
            valX, valY = data.validation_set(config.batch_size)
            _, val_loss = sess.run([m.output, m.loss], feed_dict={m.input: valX, m.target: valY})
            print("Epoch: ", epoch, "Validation Loss: ", val_loss)


if __name__ == "__main__":
    tf.app.run()