
from __future__ import division, print_function

import numpy as np

from math import cos
from math import radians
from math import sin
from random import uniform
settings = {
    "default_size":10,
    "default_speed":0.01,
    "max_energy":5,
    }
class organism():
    def __init__(self, settings, neural_matrix = None, name=None):

        self.x = uniform(settings['x_min'], settings['x_max'])  # position (x)
        self.y = uniform(settings['y_min'], settings['y_max'])  # position (y)

        self.r = uniform(0,360)                 # orientation   [0, 360]

        self.speed = settings["default_speed"]
        self.v = self.speed
        self.size = settings["default_size"]
        self.health = self.size
        self.food_count = self.size/2  # fitness (food count)
        self.layers_number = 2
        self.neurons_number_in_layer = 5
        self.name = name
        self.intelegence = 1
        self.neural_matrix = neural_matrix
        if not neural_matrix:
            self.neural_matrix = []
            self.neural_matrix.append(np.random.uniform(-1, 1, self.neurons_number_in_layer,  self.intelegence))
            for i in range(self.layers_number-2):
                self.neural_matrix.append(np.random.uniform(-1, 1, self.neurons_number_in_layer, self.neurons_number_in_layer))
            self.neural_matrix.append(np.random.uniform(-1, 1, self.neurons_number_in_layer, 1)) #only direction for now

        self.d_food = 100   # distance to nearest food
        self.r_food = 0     # orientation to nearest food




    # NEURAL NETWORK
    def think(self, feature_vector):

        # SIMPLE MLP
        af = lambda x: np.tanh(x)               # activation function
        feature_slice = feature_vector[0:self.intelegence]
        hl = af(np.dot(self.neural_matrix[0], self.r_food))
        for i in range(1,len(self.neural_matrix)-2):
            hl = af(np.dot(self.neural_matrix[i], hl))
        out =  af(np.dot(np.dot(self.neural_matrix[self.neural_matrix[-1]], hl)))


        self.nn_dr = float(out)   # [-1, 1]  (left=1, right=-1)


    # UPDATE HEADING
    def update_r(self, settings):
        self.r += self.nn_dr * settings['dr_max'] * settings['dt']
        self.r = self.r % 360


    # UPDATE VELOCITY
    def update_vel(self, settings):
        #self.v += self.nn_dv * settings['dv_max'] * settings['dt']
        #if self.v < 0: self.v = 0
        #if self.v > settings['v_max']: self.v = settings['v_max']
        self.v =  self.speed


    # UPDATE POSITION
    def update_pos(self, settings):
        dx = self.v * cos(radians(self.r)) * settings['dt']
        dy = self.v * sin(radians(self.r)) * settings['dt']
        self.x += dx
        self.y += dy

class food():
    def __init__(self, settings):
        self._x = uniform(settings['x_min'], settings['x_max'])
        self._y = uniform(settings['y_min'], settings['y_max'])
        self._energy = random.randint(1,settings["max_energy"])

    def _get_energy(self):
        return self._radius
    def _get_x(self):
        return self._x
    def _get_y(self):
        return self._y

