# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long, too-many-instance-attributes
import random
from math import radians, sin
from random import uniform
from abc import abstractmethod
import numpy as np
from numpy import cos
import settings



class Life:
    def __init__(self, num: int, neural_matrix=None, name=None):
        # position
        self.position_x = 0
        self.position_y = 0
        self.number = num
        # direction

        # organism properties
        self.number = 0
        self.ready_for_sex = 0
        self.speed = 0
        self.velocity = 0
        self.size = 0
        self.ready_for_sex = 0
        self.food_count = self.size / 2  # fitness (food count)
        self.d_food = 0
        self.r_food = 0  # orientation to nearest food
        self.vision_range = 0
        self.current_direction = 0

        # neural settings
        self.layers_number = 0
        self.neurons_number_in_layer = 0
        self.name = name

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

    @abstractmethod
    def mutate(self, sett):
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


class Organism(Life):
    def __init__(self, num: int,
                 sett, neural_matrix=None, name=None):
        super().__init__(num)
        # position
        self.position_x = uniform(0, int(sett['field_x']))  # position (x)
        self.position_y = uniform(0, int(sett['field_y']))  # position (y)
        # direction

        # organism properties
        self.number = num
        self.speed = int(sett["default_speed"])
        self.velocity = self.speed
        self.size = int(sett["default_size"])
        self.health = self.size
        self.food_count = self.size / 2  # fitness (food count)
        self.ready_for_sex = 3 / 4
        self.vision_range = 1
        self.current_direction = 0

        # neural settings
        self.layers_number = 4
        self.neurons_number_in_layer = 3
        self.name = name
        self.max_rot_speed = 15
        self.max_move_speed = 0.02
        self.neural_matrix = neural_matrix

        # features
        self.features_dict = settings.full_features_dict
        self.features_list = []

        self.decisions_dict = settings.decisions_dict

        self.mut_factor = int(sett["mut_factor"])
        self.neural_matrix = []

        self.generation = 1
        if not neural_matrix:
            self.neural_matrix = []
            self.neural_matrix.append(np.random.uniform(-1, 1, (len(self.features_dict), self.neurons_number_in_layer)))
            for _ in range(self.layers_number - 2):
                self.neural_matrix.append(
                    np.random.uniform(-1, 1, (self.neurons_number_in_layer, self.neurons_number_in_layer)))
            self.neural_matrix.append(
                np.random.uniform(-1, 1, (self.neurons_number_in_layer, len(settings.decisions_dict))))
        else:
            self.neural_matrix = neural_matrix

    def mutate(self, sett):

        n_neural = []
        for matrix in self.neural_matrix:
            n_neural.append(matrix * (1 + uniform(-self.mut_factor / 100, self.mut_factor / 100)))
        new_org = Organism(10000 + self.number, sett=sett, neural_matrix=n_neural)
        new_org.position_x = self.position_x + uniform(-0.05, 0.05)
        new_org.position_y = self.position_y + uniform(-0.05, 0.05)
        new_org.food_count = self.size / 2  # fitness (food count)
        self.food_count = self.size / 2  # fitness (food count)
        new_org.generation = self.generation + 1
        return new_org

    # NEURAL NETWORK
    def think(self):

        def activation(value):
            return np.tanh(value)
        # SIMPLE MLP
        if len(self.features_list) > 0:
            list_of_features = np.array(self.features_list).reshape(1, 3)

            activation_func = activation  # activation function
            hidden_layer = activation_func(np.dot(list_of_features, self.neural_matrix[0]))
            for matr in self.neural_matrix[1:]:
                hidden_layer = activation_func(np.dot(hidden_layer, matr))
            out = hidden_layer.reshape(3, )  # af(np.dot(hl, self.neural_matrix[len(self.neural_matrix)-1]))
            self.current_speed = out[0]
            self.current_rotation_speed = out[1]
            self.desired_direction = out[2]
        else:
            self.current_speed = uniform(0, self.max_move_speed)
            self.current_rotation_speed = uniform(0, self.max_rot_speed)
            self.desired_direction = random.randint(0, 360)

        self.update_r()
        self.update_vel()
        self.update_pos()

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

        self.velocity = self.current_speed

    # UPDATE POSITION
    def update_pos(self):
        delta_x = self.velocity * cos(radians(self.current_direction))
        delta_y = self.velocity * sin(radians(self.current_direction))
        self.position_x += delta_x
        self.position_y += delta_y
        if self.position_x > 1:
            self.position_x -= 1
        if self.position_y > 1:
            self.position_y -= 1
        if self.position_x < 0:
            self.position_x += 1
        if self.position_y < 0:
            self.position_y += 1
