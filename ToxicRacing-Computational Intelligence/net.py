from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten

from keras.layers import Conv2D, MaxPooling2D,LSTM,Embedding
from keras import backend as K
import csv
import os
import numpy as np
batch_size = 128
num_classes = 3
epochs = 12

# input image dimensions
inputs=22
img_rows, img_cols = 28, 28
directo=os.getcwd()
foo=directo+"/train_data/aalborg.csv"



from numpy import genfromtxt
data = genfromtxt(foo, delimiter=',',skip_header=1,skip_footer=1)

# data=np.delete(my_data[:],4,1)

# data=np.concatenate((my_data[:][:4],my_data[:][4:]),axis=0)
print(data.shape)
data=data[:-3]
# print(my_data[:1][])
# print(my_data[:1][4:])
x_data=np.zeros((len(data)-2,2))
y_data=np.zeros((len(data)-2,1))


for i in range(1,len(data)-4):
  for j in range(len(data[3])):
    if j ==2:

      y_data[i][0]=data[i][j]
    
      
        # if j>4:

        #   x_data[i][j-3]=data[i][j]/200
        # else:

    elif j==3:
        x_data[i][0]=data[i][j]/200

        
    elif j==5:

        x_data[i][1]=data[i][j]

x_data=np.reshape(x_data,(((int(len(x_data)/5))),5,2))
y_data=y_data[::5]
# print(x_data)
# for i in range(1,len(x_data)):
#   for j in range(3,len(x_data)):
#     # print(x_data[i][j])
#     x_data[i][j]=float(x_data[i][j]/200)


print("blah",x_data[1])

print("meh",np.asarray(x_data).shape,"dasugi")

print("this",y_data.shape)
print("this",x_data.shape)
# t=int(len(x_data)/80)
# x_train=np.asarray(x_data[:][t:])
# x_test=np.asarray(x_data[:][:t])
# y_train=np.asarray(y_data[:][t:])
# y_test=np.asarray(y_data[:][:t])
# print("thismeh",y_train[-20])
# print("thismeh",x_train[-20])
# print("thismeh",y_test[-20])
# print("thismeh",x_test[-20])

# xt=np.reshape(x_data,(len(x_data),1,2))
# yt=np.reshape(y_data,(-1,1))
# xte=np.reshape(x_test,(len(x_test),1,2))
# yte=np.reshape(y_test,(-1,1))
# print(xt.shape,y_train.shape)
# keras_model_sequential() %>%
#   layer_lstm(units = 16, input_shape = c(2, 110))  %>%
#   layer_dense(units = 1) %>%
#   layer_activation('sigmoid') %>%
#   compile(loss = 'binary_crossentropy', 
#           optimizer = 'adam', 
#           metrics = 'accuracy')
# # Start neural network
model = Sequential()

model.add(LSTM(units = 100, input_shape = (5, 2)))
# model.add(Dense(200, activation='relu'))
# model.add(Dense(100, activation='relu'))
model.add(Dense(50, activation='relu'))
model.add(Dense(25, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))
# 3

from keras.models import model_from_json
import keras
tbCallBack = keras.callbacks.TensorBoard(log_dir='/tmp/keras_logs', write_graph=True)

# 4
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
score=model.fit(x_data, y_data, epochs=100, batch_size=10,  verbose=1, validation_split=0.4, callbacks=[tbCallBack])
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
# print(x_test[5])
# X=np.zeros((1,22))
# for i in range(len(x_test[5])):
#   X[0][i]=x_test[5][i]

# # X[0][0]=   x_test[5]
# loaded_model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

# y=loaded_model.predict( xte, batch_size=1, verbose=1)


# print(y)

