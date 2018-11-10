import os
from numpy import genfromtxt
import numpy as np
from sklearn import preprocessing


def getAccelarator(state):
    if state.speed_x < 70:
        return 1
    else:
        return 0


def getGear(state):
    if state.gear == 0:
        return 1
    elif state.rpm > 8000:
        return state.gear + 1
    elif state.rpm < 3000:
        return state.gear - 1


def getData(path):
    directo = os.getcwd()
    path = directo + path
    my_data = genfromtxt(path, delimiter=',', skip_header=1, skip_footer=1)

    x_data = np.zeros((len(my_data) - 2, 22))
    y_data = np.zeros((len(my_data) - 2, 3))

    x_data = preprocessing.normalize(x_data)
    for i in range(1, len(my_data) - 2):
        for j in range(len(my_data[3])):
            if j < 3:
                y_data[i][j] = my_data[i][j]
            else:
                x_data[i][j - 3] = my_data[i][j]
    return np.array(x_data), np.array(y_data)
