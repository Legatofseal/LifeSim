from __future__ import division, print_function

from time import sleep

import numpy as np

from math import cos, sqrt, degrees, atan2
from math import radians
from math import sin
from random import uniform
from collections import OrderedDict
import random

from matplotlib.patches import Circle

from plotting import plot_food
from plotting import plot_organism

from matplotlib import pyplot as plt, lines

settings = {
    "default_size": 10,
    "default_speed": 0.01,
    "max_energy": 5,
    "field_x": 100,
    "field_y": 100,
    "max_speed": 2,

}
full_features_dict = OrderedDict([("food_distance", 0), ("food_size", 0), ("org_around_food", 0)])
decisions_dict = OrderedDict([("current_speed", 0), ("current_rotation_speed", 0), ("desired_direction", 0)])

fig, ax = plt.subplots()
fig.set_size_inches(9.6, 5.4)

plt.xlim(0, settings["field_x"])
plt.ylim(0, settings["field_y"])


def dist(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calc_heading(org, food):
    d_x = food.x - org.x
    d_y = food.y - org.y
    theta_d = degrees(atan2(d_y, d_x)) - org.r
    if abs(theta_d) > 180: theta_d += 360
    return theta_d / 180


class organism():
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
        self.vision_range = 2
        self.current_direction = 0

        # neural settings
        self.layers_number = 2
        self.neurons_number_in_layer = 5
        self.name = name
        self.intelegence = 2
        self.dexterity = 5
        self.neural_matrix = neural_matrix

        # features
        self.features_dict = full_features_dict

        # decisions
        self.current_speed = 0
        self.current_rotation_speed = 0
        self.desired_direction = 0

        self.decisions_dict = decisions_dict

        if not neural_matrix:
            self.neural_matrix = []
            self.neural_matrix.append(np.random.uniform(-1, 1, self.neurons_number_in_layer, len(self.features_dict)))
            for i in range(self.layers_number - 2):
                self.neural_matrix.append(
                    np.random.uniform(-1, 1, self.neurons_number_in_layer, self.neurons_number_in_layer))
            self.neural_matrix.append(
                np.random.uniform(-1, 1, self.neurons_number_in_layer, len(decisions_dict)))  # only direction for now

    # NEURAL NETWORK
    def think(self, feature_vector):

        # SIMPLE MLP
        af = lambda x: np.tanh(x)  # activation function
        feature_slice = feature_vector[0:self.intelegence]
        hl = af(np.dot(self.neural_matrix[0], self.r_food))
        for i in range(1, len(self.neural_matrix) - 2):
            hl = af(np.dot(self.neural_matrix[i], hl))
        out = af(np.dot(np.dot(self.neural_matrix[self.neural_matrix[-1]], hl)))
        self.current_speed = out[0]
        self.current_rotation_speed = out[1]
        self.desired_direction = out[2]

    # UPDATE HEADING
    def update_r(self):
        if self.current_rotation_speed > 2:
            self.current_rotation_speed = self.dexterity
        if self.current_rotation_speed < -2:
            self.current_rotation_speed = -self.dexterity
        self.current_direction += self.current_rotation_speed
        self.current_direction = self.current_rotation_speed

        self.current_direction = self.current_direction % 360

    # UPDATE VELOCITY
    def update_vel(self, settings):
        # self.v += self.nn_dv * settings['dv_max'] * settings['dt']
        # if self.v < 0: self.v = 0
        # if self.v > settings['v_max']: self.v = settings['v_max']
        self.v = self.speed

    # UPDATE POSITION
    def update_pos(self, settings):
        dx = self.v * cos(radians(self.current_direction))
        dy = self.v * sin(radians(self.current_direction))
        self.x += dx
        self.y += dy


class food_f():
    def __init__(self, settings):
        self._x = uniform(settings['x_min'], settings['x_max'])
        self._y = uniform(settings['y_min'], settings['y_max'])
        self._energy = random.randint(1, settings["max_energy"])

    def _get_energy(self):
        return self._energy

    def _get_x(self):
        return self._x

    def _get_y(self):
        return self._y


def simulate(organisms, foods_list):
    # UPDATE FITNESS FUNCTION
    for food in foods_list:
        for org in organisms:
            food_org_dist = dist(org.x, org.y, food.x, food.y)

            # UPDATE FITNESS FUNCTION
            if food_org_dist <= 0.075:
                org.food_count += food.energy

            # RESET DISTANCE AND HEADING TO NEAREST FOOD SOURCE
            org.d_food = 100
            org.r_food = 0

    for org in organisms:
        org.food_count -= 0.1
        if food.food_count <= 0:
            organisms.remove(org)

    for food in foods_list:
        if food.energy <= 0:
            foods.remove(food)
    # CALCULATE HEADING TO NEAREST FOOD SOURCE
    for food in foods_list:
        for org in organisms:

            # CALCULATE DISTANCE TO SELECTED FOOD PARTICLE
            food_org_dist = dist(org.x, org.y, food.x, food.y)

            # DETERMINE IF THIS IS THE CLOSEST FOOD PARTICLE
            if food_org_dist < org.d_food:
                org.d_food = food_org_dist
                org.r_food = calc_heading(org, food)

    # GET ORGANISM RESPONSE
    for org in organisms:
        org.think()

    # UPDATE ORGANISMS POSITION AND VELOCITY
    for org in organisms:
        org.update_r(settings)
        org.update_vel(settings)
        org.update_pos(settings)

    return organisms


def plot_frame(organisms, foods):
    plt.clf()
    # PLOT ORGANISMS
    for organism in organisms:
        circle = Circle([organisms.x, organisms.y], 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
        ax.add_artist(circle)

        edge = Circle([organisms.x, organisms.y], 0.05, facecolor='None', edgecolor='darkgreen', zorder=8)
        ax.add_artist(edge)

        tail_len = 0.075

        x2 = cos(radians(organisms.current_direction)) * tail_len + organisms.x
        y2 = sin(radians(organisms.current_direction)) * tail_len + organisms.y

        ax.add_line(lines.Line2D([organisms.x, x2], [organisms.y, y2], color='darkgreen', linewidth=1, zorder=10))

    # PLOT FOOD PARTICLES
    for food in foods:
        circle = Circle([food.x, food.y], 0.03, edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
        ax.add_artist(circle)

    # MISC PLOT SETTINGS
    ax.set_aspect('equal')
    frame = plt.gca()
    frame.axes.get_xaxis().set_ticks([])
    frame.axes.get_yaxis().set_ticks([])

    plt.figtext(0.025, 0.95, r'GENERATION: ' + str(0))
    plt.show()


amebas = [organism(x) for x in range(1,10)]
foods = [food_f() for x in range(1,100)]

while True:
    simulate(amebas,foods)
    plot_frame(amebas.food)
    sleep(1.0)