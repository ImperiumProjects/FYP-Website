import pandas as pd
import numpy as np

from keras.models import Sequential
from keras.layers import SimpleRNN
from keras.layers import GRU
from keras.layers import Dense
from keras.optimizers import RMSprop
from keras.callbacks import EarlyStopping

from sqlalchemy import create_engine
import pymysql

###############################################################################
#
# Credit:
#
# This code is loosely based on the artificial intelligence II
# course material presented by Dr. Derek Bridge, Recurrent Neural Network 
# Examples, 2018
#
###############################################################################

engine = 'mysql+mysqldb://scraper:scraper@84.200.193.29:3306/historical'
conn = create_engine(engine)
conn.connect()
trans = conn.begin()

#
# Reading the data directly from the remote database
# directly into a pandas dataframe
#
historical_data_df = pd.read_sql("select * from two_point_data", conn)

historical_array = historical_data_df[["level"]].astype(float).values

# Standard scaling
# Compute means and standard deviations on the training data
means = historical_array[:val_start_idx].mean(axis=0)
stds = historical_array[:val_start_idx].std(axis=0)

# Standardize all the data
historical_array -= means
historical_array /= stds

def data_generator(array, min_idx, max_idx, seq_length, delay, batch_size):
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

#
# seq_length = 672 (this is due to our dataset being in intervals of 
# 15 minutes, meaning if we want sequences of 1 week long, our calculation
# is formed by 7, the days in the week, and 96, the number of 15 minute
# segments in a day == 7 * 96 = 672)
#
# delay = 168 (this value is the range of time we want to predict into the
# future, in this case 7 * 24 == 168, for predicting 1 week in advance)
#
one_week_generator = data_generator(historical_array, min_idx = 0, max_idx = None, seq_length = 672,
    delay = 168, batch_size = 64)

#
# delay = 336 (this value is the range of time we want to predict into the
# future, in this case 14 * 24 == 168, for predicting 2 weeks in advance)
#
two_week_generator = data_generator(historical_array, min_idx = 0, max_idx = None, seq_length = 672,
    delay = 336, batch_size = 64)

#
# delay = 672 (this value is the range of time we want to predict into the
# future, in this case 28 * 24 == 168, for predicting 1 month in advance)
#
# Unrelated fun fact, there are the same amount of hours in a 28-day
# month as there are 15 minute segments in a day, who knew?
#
one_month_generator = data_generator(historical_array, min_idx = 0, max_idx = None, seq_length = 672,
    delay = 672, batch_size = 64)

def to_meters(level):
    return level * stds[0]

def build_rnn():
    network = Sequential()
    network.add(SimpleRNN(32, activation="tanh", input_shape=(None, 1)))
    network.add(Dense(1, activation="linear"))
    network.compile(optimizer=RMSprop(), loss="mse", metrics=["mae"])
    return network

network = build_rnn()

#
# One week section
#
one_week_prediction = network.predict_generator(
    self, one_week_generator, steps=500, max_queue_size=10, 
    workers=4, use_multiprocessing=True, verbose=0)

one_week_value = one_week_prediction.to_meters()
conn.execute("INSERT INTO seven_day_forecast VALUES (?)", one_week_value)

#
# Two week section
#
two_week_prediction = network.predict_generator(
    self, two_week_generator, steps=500, max_queue_size=10, 
    workers=4, use_multiprocessing=True, verbose=0)

two_week_value = two_week_prediction.to_meters()
conn.execute("INSERT INTO two_week_forecast VALUES (?)", two_week_value)

#
# One month section
#
one_month_prediction = network.predict_generator(
    self, one_month_generator, steps=500, max_queue_size=10, 
    workers=4, use_multiprocessing=True, verbose=0)

one_month_value = one_month_prediction.to_meters()
conn.execute("INSERT INTO one_month_forecast VALUES (?)", one_month_value)

trans.commit()

conn.close()