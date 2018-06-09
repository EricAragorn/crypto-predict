# Credit to Tensorflow authors: https://github.com/tensorflow/models/tree/master/tutorials/rnn/ptb

"""
An LSTM model to estimate scalar targets from time series
"""

import tensorflow as tf


class LSTMModel:
    def __init__(self, is_training, model_config):
        self._hidden_size = model_config.hidden_size
        self._num_steps = model_config.num_steps
        self._batch_size = model_config.batch_size
        self._lr = tf.Variable(0.0, trainable=False)

        self.input = tf.placeholder(tf.float32, [self._batch_size, self._num_steps, model_config.feature_size])
        self.target = tf.placeholder(tf.float32, [self._batch_size, model_config.target_size])

        lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(self._hidden_size, forget_bias=0.0, state_is_tuple=True, activation=tf.nn.relu)
        if is_training and model_config.dropout_prob > 0:
            lstm_cell = tf.nn.rnn_cell.DropoutWrapper(lstm_cell, output_keep_prob=1 - model_config.dropout_prob)

        cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell] * model_config.num_layers, state_is_tuple=True)
        self._initial_state = cell.zero_state(batch_size=self._batch_size, dtype=tf.float32)

        inputs = self.input
        if is_training and model_config.dropout_prob > 0:
            inputs = tf.nn.dropout(inputs, 1 - model_config.dropout_prob)

        with tf.variable_scope("lstm"):
            lstm_outputs = []
            state = self._initial_state
            for time_step in range(self._num_steps):
                if time_step > 0:
                    tf.get_variable_scope().reuse_variables()
                (output, state) = cell(inputs[:, time_step, :], state=state)
                lstm_outputs.append(output)

            lstm_outputs = tf.concat(lstm_outputs, 1)

        with tf.variable_scope("dense", reuse=False):
            h1 = tf.layers.dense(inputs=lstm_outputs,
                                 units=1500,
                                 activation=tf.nn.tanh,
                                 kernel_initializer=tf.initializers.truncated_normal(stddev=0.1),
                                 bias_initializer=tf.initializers.zeros(),
                                 name="hidden1")

        with tf.variable_scope("dropout", reuse=False):
            d1 = tf.layers.dropout(inputs=h1,
                                   rate=model_config.dropout_prob)

        with tf.variable_scope("dense", reuse=False):
            output = tf.layers.dense(inputs=d1,
                                     units=model_config.target_size,
                                     kernel_initializer=tf.initializers.truncated_normal(stddev=0.1),
                                     bias_initializer=tf.initializers.zeros())

        # Loss function: squared error
        self.loss = tf.div(tf.reduce_sum(tf.square(output - self.target)), model_config.batch_size)
        optimizer = tf.train.AdamOptimizer(self._lr)
        grad_and_var = optimizer.compute_gradients(self.loss)
        grad_and_var = [(tf.clip_by_norm(grad, model_config.max_grad_norm),tvars) for grad, tvars in grad_and_var]
        self.train_op = optimizer.apply_gradients(grad_and_var)


        self._new_lr = tf.placeholder(tf.float32, [])
        self.update_lr = tf.assign(self._lr, self._new_lr)
