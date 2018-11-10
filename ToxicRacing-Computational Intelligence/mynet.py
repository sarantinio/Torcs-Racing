
from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.layers import LSTM
import csv
import os
import numpy as np
from numpy import genfromtxt


batch_size = 128
num_classes = 3
epochs = 12
inputs=22
img_rows, img_cols = 28, 28
directo=os.getcwd()
foo=directo+"/train_data/aalborg.csv"



my_data = genfromtxt(foo, delimiter=',',skip_header=1,skip_footer=1)
print(my_data.shape)
x_data=np.zeros((len(my_data)-2,22))
y_data=np.zeros((len(my_data)-2,3))


for i in range(1,len(my_data)-2):
  for j in range(len(my_data[3])):
    if j <3:

      y_data[i][j]=my_data[i][j]
    else:
      x_data[i][j-3]=my_data[i][j]


t=int(len(x_data)/80)
x_train=np.asarray(x_data[:][t:])
x_test=np.asarray(x_data[:][:t])
y_train=np.asarray(y_data[:][t:])
y_test=np.asarray(y_data[:][:t])

model = Sequential()
model.add(LSTM(50, input_shape=(22,)))
# model.add(Dense(50, init='normal', activation='sigmoid'))
# model.add(Dense(55, init='normal', activation='sigmoid'))
# model.add(Dense(12, init='normal', activation='sigmoid'))
model.add(Dense(1, init='normal', activation='sigmoid'))
model.summary()

# 3
from keras.models import model_from_json
import keras
tbCallBack = keras.callbacks.TensorBoard(log_dir='/tmp/keras_logs', write_graph=True)

# 4
model.compile(loss='mae', optimizer='adam', metrics=['accuracy'])
score=model.fit(x_data, y_data, epochs=250, batch_size=50,  verbose=1, validation_split=0.3, callbacks=[tbCallBack])
# model.predict( x_test, batch_size=22, verbose=0)
# score = model.evaluate(x_test, y_test, verbose=0)
print(score)
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
 
with open('model.json', 'r') as json_file:
  loaded_model_json = json_file.read()
json_file.close() 
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model.h5")
# print("Loaded model from disk")
print(x_test[5])
X=np.zeros((1,22))
for i in range(len(x_test[5])):
  X[0][i]=x_test[5][i]

# X[0][0]=   x_test[5]
loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

y=loaded_model.predict( X, batch_size=1, verbose=1)


print(y)

