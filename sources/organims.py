from math import radians, sin
from random import uniform, random
import numpy as np
from numpy import cos
import settings
from abc import abstractmethod


class life():
    def __init__(self, num: int, neural_matrix=None, name=None):
        # position
        self.x = 0
        self.y = 0
        # direction

        # organism properties
        self.number = 0
        self.speed = 0
        self.v = 0
        self.size = 0
        self.food_count = self.size / 2  # fitness (food count)
        self.d_food = 0
        self.r_food = 0  # orientation to nearest food
        self.vision_range = 0
        self.current_direction = 0

        # neural settings
        self.layers_number = 0
        self.neurons_number_in_layer = 0
        self.name = name
        self.intelegence = 0
        self.max_rot_speed = 0
        self.max_move_speed = 0
        self.neural_matrix = neural_matrix

        # features
        self.features_dict = 0
        self.features_list = []
        # decisions
        self.current_speed = 0
        self.current_rotation_speed = 0
        self.desired_direction = 0

        self.decisions_dict = settings.decisions_dict

        self.mut_factor = 0
        self.neural_matrix = []

        self.generation = 1
        if not neural_matrix:
            self.neural_matrix = []
            self.neural_matrix.append(np.random.uniform(-1, 1, (len(self.features_dict), self.neurons_number_in_layer)))
            for i in range(self.layers_number - 2):
                self.neural_matrix.append(
                    np.random.uniform(-1, 1, (self.neurons_number_in_layer, self.neurons_number_in_layer)))
            self.neural_matrix.append(
                np.random.uniform(-1, 1, (self.neurons_number_in_layer, len(settings.decisions_dict))))
        else:
            self.neural_matrix = neural_matrix

    @abstractmethod
    def mutate(self):
        return

    @abstractmethod
    def think(self):
        return

    @abstractmethod
    def update_r(self):
        return

    @abstractmethod
    def update_vel(self):
        return

    @abstractmethod
    def update_pos(self):
        return


class organism(life):
    def __init__(self, num: int, neural_matrix=None, name=None):
        # position
        self.x = uniform(0, settings['field_x'])  # position (x)
        self.y = uniform(0, settings['field_y'])  # position (y)
        # direction

        # organism properties
        self.number = num
        self.speed = settings["default_speed"]
        self.v = self.speed
        self.size = settings["default_size"]
        self.health = self.size
        self.food_count = self.size / 2  # fitness (food count)
        self.d_food = 100  # distance to nearest food
        self.r_food = 0  # orientation to nearest food
        self.vision_range = 1
        self.current_direction = 0

        # neural settings
        self.layers_number = 4
        self.neurons_number_in_layer = 3
        self.name = name
        self.intelegence = 2
        self.max_rot_speed = 15
        self.max_move_speed = 0.02
        self.neural_matrix = neural_matrix

        # features
        self.features_dict = settings.full_features_dict
        self.features_list = []
        # decisions
        self.current_speed = 0
        self.current_rotation_speed = 0
        self.desired_direction = 0

        self.decisions_dict = settings.decisions_dict

        self.mut_factor = settings["mut_factor"]
        self.neural_matrix = []

        self.generation = 1
        if not neural_matrix:
            self.neural_matrix = []
            self.neural_matrix.append(np.random.uniform(-1, 1, (len(self.features_dict), self.neurons_number_in_layer)))
            for i in range(self.layers_number - 2):
                self.neural_matrix.append(
                    np.random.uniform(-1, 1, (self.neurons_number_in_layer, self.neurons_number_in_layer)))
            self.neural_matrix.append(
                np.random.uniform(-1, 1, (self.neurons_number_in_layer, len(settings.decisions_dict))))
        else:
            self.neural_matrix = neural_matrix

    def mutate(self):

        n_neural = []
        for m in self.neural_matrix:
            n_neural.append(m * (1 + uniform(-self.mut_factor / 100, self.mut_factor / 100)))
        n = organism(10000 + self.number, n_neural)
        n.x = self.x + uniform(-0.05, 0.05)
        n.y = self.y + uniform(-0.05, 0.05)
        n.food_count = self.size / 2  # fitness (food count)
        self.food_count = self.size / 2  # fitness (food count)
        n.generation = self.generation + 1
        return n

    # NEURAL NETWORK
    def think(self):

        # SIMPLE MLP
        if len(self.features_list) > 0:
            list_of_features = np.array(self.features_list).reshape(1, 3)

            af = lambda x: np.tanh(x)  # activation function
            hl = af(np.dot(list_of_features, self.neural_matrix[0]))
            for matr in self.neural_matrix[1:]:
                hl = af(np.dot(hl, matr))
            out = hl.reshape(3, )  # af(np.dot(hl, self.neural_matrix[len(self.neural_matrix)-1]))
            self.current_speed = out[0]
            self.current_rotation_speed = out[1]
            self.desired_direction = out[2]
        else:
            self.current_speed = uniform(0, self.max_move_speed)
            self.current_rotation_speed = uniform(0, self.max_rot_speed)
            self.desired_direction = random.randint(0, 360)

    # UPDATE HEADING

    def update_r(self):
        '''
        if self.current_rotation_speed > self.max_rot_speed:
            self.current_rotation_speed = self.max_rot_speed
        if self.current_rotation_speed < -self.max_rot_speed:
            self.current_rotation_speed = -self.max_rot_speed
        '''
        self.current_rotation_speed = abs(self.current_rotation_speed) * self.max_rot_speed
        self.current_direction += self.current_rotation_speed
        self.current_direction = self.current_direction % 360

    # UPDATE VELOCITY
    def update_vel(self):
        if self.current_speed > self.max_move_speed:
            self.current_speed = self.max_move_speed
        if self.current_speed < -self.max_move_speed:
            self.current_speed = -self.max_move_speed

        self.v = self.current_speed

    # UPDATE POSITION
    def update_pos(self):
        dx = self.v * cos(radians(self.current_direction))
        dy = self.v * sin(radians(self.current_direction))
        self.x += dx
        self.y += dy
        if self.x > 1:
            self.x -= 1
        if self.y > 1:
            self.y -= 1
        if self.x < 0:
            self.x += 1
        if self.y < 0:
            self.y += 1
