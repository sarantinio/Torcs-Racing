from __future__ import print_function
from keras.datasets import mnist
from keras.models import Sequential
from keras.optimizers import Adam

from keras.layers import Dense, Dropout, Flatten, Input, merge
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from numpy import genfromtxt
from keras.models import model_from_json, Model

import keras
import csv
import os
import numpy as np
import keras


def train_model(x_data, y_data, name):
    score = model.fit(x_data, y_data, epochs=250, batch_size=50, verbose=1, validation_split=0.3,
                      callbacks=[tbCallBack])
    # model.predict( x_test, batch_size=22, verbose=0)
    # score = model.evaluate(x_test, y_test, verbose=0)
    print(score)
    model_json = model.to_json()
    with open((name + ".json"), "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights((name + "model.h5"))
    print("Saved model to disk")

    with open((name + '.json'), 'r') as json_file:
        loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights((name + "model.h5"))
    # print("Loaded model from disk")
    print(x_test[5])
    X = np.zeros((1, 22))
    for i in range(len(x_test[5])):
        X[0][i] = x_test[5][i]

    # X[0][0]=   x_test[5]
    loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

    y = loaded_model.predict(X, batch_size=1, verbose=1)
    print(y)


current_dir = os.getcwd()
path_to_data = current_dir + "/train_data/aalborg.csv"

my_data = genfromtxt(path_to_data, delimiter=',', skip_header=1, skip_footer=1)
### Split data into Accelaration, Brake, Steering #### 
x_data = np.zeros((len(my_data) - 2, 22))
accelaration_data = np.zeros((len(my_data) - 2, 1))
brake_data = np.zeros((len(my_data) - 2, 1))
steering_data = np.zeros((len(my_data) - 2, 1))

for i in range(1, len(my_data) - 2):
    for j in range(len(my_data[3])):
        if j == 0:
            accelaration_data[i] = my_data[i][j]
        elif j == 1:
            brake_data[i] = my_data[i][j]
        elif j == 2:
            steering_data[i] = my_data[i][j]
        else:
            x_data[i][j - 3] = my_data[i][j]

# t=int(len(x_data)/80)
# x_train=np.asarray(x_data[:][t:])
# x_test=np.asarray(x_data[:][:t])

# accelaration_train=np.asarray(accelaration_data[:][t:])
# accelaration_test=np.asarray(accelaration_data[:][:t])
# braking_train=np.asarray(brake_data[:][t:])
# braking_test=np.asarray(brake_data[:][:t])
# steering_train=np.asarray(steering_data[:][t:])
# steering_test=np.asarray(steering_data[:][:t])
HIDDEN1_UNITS = 300
HIDDEN2_UNITS = 600
state_size = 22
action_dim = 3
S = Input(shape=[state_size])
A = Input(shape=[action_dim], name='action2')
w1 = Dense(HIDDEN1_UNITS, activation='relu')(S)
a1 = Dense(HIDDEN2_UNITS, activation='linear')(A)
h1 = Dense(HIDDEN2_UNITS, activation='linear')(w1)
h2 = merge([h1, a1], mode='sum')
h3 = Dense(HIDDEN2_UNITS, activation='relu')(h2)
V = Dense(action_dim, activation='linear')(h3)
model = Model(input=[S, A], output=V)
adam = Adam(lr=0.0001)
model.compile(loss='mse', optimizer=adam)  # model.add(Dense(1, init='normal', activation='sigmoid'))

# 3
tbCallBack = keras.callbacks.TensorBoard(log_dir='/tmp/keras_logs', write_graph=True)

# 4
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
# train_model(x_data, accelaration_data, "accelaration")
train_model(x_data, steering_data, "steering")
# train_model(x_data, brake_data, "brake")
