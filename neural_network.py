import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers import SimpleRNN
from keras.layers import GRU
from keras.layers import Dense
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping

historical_data_df = pd.read_csv("riverLevels.csv")

historical_array = historical_data_df[["level"]].astype(float).values

# Indexes for splitting the data
length = len(historical_array)
val_start_idx = int(0.6 * length)
test_start_idx = int(0.8 * length)

# Standard scaling
# Compute means and standard deviations on the training data
means = historical_array[:val_start_idx].mean(axis=0)
stds = historical_array[:val_start_idx].std(axis=0)
# Standardize all the data
historical_array -= means
historical_array /= stds

def data_generator(array, min_idx, max_idx, seq_length = 672, delay = 1, batch_size = 64):
    num_variables = array.shape[-1]
    if max_idx == None:
        max_idx = len(array) - delay - 1
    i = min_idx + seq_length
    while True:
        if i + batch_size >= max_idx:
            i = min_idx + seq_length
        rows = np.arange(i, min(i + batch_size, max_idx))
        i += len(rows)
        examples = np.zeros((len(rows), seq_length, num_variables))
        targets = np.zeros((len(rows),))
        for j, row in enumerate(rows):
            examples[j] = array[row - seq_length : row]
            targets[j] = array[row + delay][0]
        yield examples, targets

train_generator = data_generator(historical_array, min_idx = 0, max_idx = val_start_idx)
val_generator = data_generator(historical_array, min_idx = val_start_idx, max_idx = test_start_idx)
test_generator = data_generator(historical_array, min_idx = test_start_idx, max_idx = None)

val_steps = test_start_idx - (val_start_idx + 1) - 24
test_steps = length - (test_start_idx + 1) - 24

def evaluate_baseline(data_generator):
    batch_maes = []
    for step in range(val_steps):
        examples, targets = next(data_generator)
        preds = examples[:, -1, 0]
        mae = np.mean(np.abs(preds - targets))
        batch_maes.append(mae)
    return np.mean(batch_maes)

def to_meters(level):
    return level * stds[0]

mae = evaluate_baseline(val_generator)

to_meters(mae)

def build_rnn():
    network = Sequential()
    network.add(SimpleRNN(32, activation="tanh", input_shape=(None, 1)))
    network.add(Dense(1, activation="linear"))
    network.compile(optimizer=RMSprop(), loss="mse", metrics=["mae"])
    return network

network = build_rnn()

history = network.fit_generator(
    train_generator, steps_per_epoch=500, epochs=20,
    validation_data=val_generator, validation_steps=val_steps,
    callbacks=[EarlyStopping(monitor="val_loss", patience=1)],
    verbose=0)

# Since patience was 1, perhaps use the validation MAE from just before that point
val_mae = history.history["val_mean_absolute_error"][-2]

to_meters(val_mae)

test_loss, test_mae = network.evaluate_generator(test_generator, steps=test_steps)

to_meters(test_mae)