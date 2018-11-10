import csv
import numpy as np
from pyESN import ESN
import driving_utils

x_data, y_data = driving_utils.getData("/train_data/aalborg.csv")
x_data1, y_data1 = driving_utils.getData("/train_data/alpine-1.csv")
x_data2, y_data2 = driving_utils.getData("/train_data/f-speedway.csv")
print(x_data.shape)
print(x_data1.shape)
print(x_data2.shape)
print(y_data.shape)
print(y_data1.shape)
print(y_data2.shape)

x_data = np.concatenate((x_data, x_data1), axis=0)
x_data = np.concatenate((x_data, x_data2), axis=0)
y_data = np.concatenate((y_data, y_data1), axis=0)
y_data = np.concatenate((y_data, y_data2), axis=0)
print(y_data.shape)
print(x_data.shape)
rng = np.random.RandomState(42)
esn = ESN(n_inputs=22,
          n_outputs=3,
          n_reservoir=2000,
          spectral_radius=1.5,
          random_state=42)
esn.fit(x_data, y_data, inspect=True)


def predict(X):
    return esn.predict(X)
