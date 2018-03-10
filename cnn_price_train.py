import tensorflow as tf
import numpy as np

def cnn_model_fun(features, targets, mode):
    input_layer = tf.reshape(features["x"], (-1, 60, 1, 5))
    conv1 = tf.layers.conv1d(
        inputs=input_layer,
        filter=32,
        kernel_size=5,
        activation=None
    )
    pool1 = tf.layers.average_pooling1d(
        inputs=conv1,
        pool_size=2,
        strides=2
    )
    conv2 = tf.layers.conv1d(
        inputs=pool1,
        filter=64,
        kernel_size=5,
        activation=None,
    )
    pool2 = tf.layers.average_pooling1d(
        inputs=conv2,
        pool_size=2,
        strides=2
    )

    pool2_flat = tf.reshape(pool2, [-1, 12*64])
    dense1 = tf.layers.dense(
        inputs=pool2_flat,
        units=128,
    )

    dropout = tf.layers.dropout(
        inputs=dense1,
        rate=0.4,
        training=mode == tf.estimator.ModeKeys.TRAIN
    )

    output = tf.layers.dense(
        inputs=dropout,
        units=1
    )

    predictions = {
        "price": output
    }
    if mode == tf.estimator.ModeKeys.PREDICT:
        return tf.estimator.EstimatorSpec(mode=mode, predictions=predictions)

    loss = tf.losses.mean_squared_error(
        labels=targets,
        predictions=output
    )