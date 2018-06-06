
# features used for prediction and targets
feature_list = ["open", "high", "low", "close", "vwap", "volume", "count",
                "ask price5", "ask volume5", "ask price4", "ask volume4",
                "ask price3", "ask volume3", "ask price2", "ask volume2",
                "ask price1", "ask volume1", "bid price1", "bid volume1",
                "bid price2", "bid volume2", "bid price3", "bid volume3",
                "bid price4", "bid volume4", "bid price5", "bid volume5"]

target_list = ["high", "low"]
feature_size = len(feature_list)
target_size = len(target_list)

# Run configurations
batch_size = 500  # training batch size
num_steps = 60  # number of records feed into LSTM
time_lap = 30  # time lap between last record of input and target record
training_ratio = 0.75  # ratio of training set to data set
initial_lr = 0.02
lr_decay_rate = 0.8
max_epoches = 60
decay_range = 40  # start weight decay after epoch exceeds range

# LSTM settings
hidden_size = feature_size  # hidden units of a single LSTM cell
dropout_prob = 0.1  # dropout_
num_layers = 5
