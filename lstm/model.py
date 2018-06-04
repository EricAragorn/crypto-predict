# Credit to Tensorflow authors: https://github.com/tensorflow/models/tree/master/tutorials/rnn/ptb

import tensorflow as tf
import config

class LSTMModel:
    def __init__(self, is_training):
        self._hidden_size = config.hidden_size
        self._num_steps = config.num_steps
        self._batch_size = config.batch_size
        self._lr = config.initial_lr

        self.input = tf.placeholder(tf.float32, [self._batch_size, self._num_steps, config.feature_size])
        self.target = tf.placeholder(tf.float32, [self._batch_size, config.target_size])

        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(self._hidden_size, forget_bias=0.0, state_is_tuple=True, activation=tf.nn.relu)
        if is_training and config.dropout_prob > 0:
            lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=1 - config.dropout_prob)

        cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell] * config.num_layers, state_is_tuple=True)
        self._initial_state = cell.zero_state(batch_size=self._batch_size, dtype=tf.float32)

        inputs = self.input
        if is_training and config.dropout_prob > 0:
            inputs = tf.nn.dropout(inputs, 1 - config.dropout_prob)

        with tf.variable_scope("lstm_output"):
            lstm_outputs = []
            state = self._initial_state
            for time_step in range(self._num_steps):
                if time_step > 0: tf.get_variable_scope().reuse_variables()
                (output, state) = cell(inputs[:, time_step, :], state=state)
                lstm_outputs.append(output)

            lstm_outputs = tf.concat(lstm_outputs, 1)

        with tf.variable_scope("foo", reuse=False):
            h1 = tf.layers.dense(inputs=lstm_outputs,
                                 units=1024,
                                 activation=tf.nn.tanh,
                                 kernel_initializer=tf.initializers.truncated_normal(stddev=0.1),
                                 bias_initializer=tf.initializers.zeros(),
                                 name="hidden1")
            d1 = tf.layers.dropout(inputs=h1,
                                   rate=config.dropout_prob)

            self.output = tf.layers.dense(inputs=d1,
                                          units=2,
                                          kernel_initializer=tf.initializers.truncated_normal(stddev=0.1),
                                          bias_initializer=tf.initializers.constant(0.1))

            self.loss = tf.reduce_sum(tf.square(self.output - self.target))
            self.train_op = tf.train.AdamOptimizer(self._lr).minimize(self.loss)

            # self._new_lr = tf.placeholder(tf.float32, [])
            # self._update_lr = tf.assign(self._lr, self._new_lr)
