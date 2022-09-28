from __future__ import division, print_function

from time import sleep

import numpy
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
from collections import Counter
settings = {
    "default_size": 10,
    "default_speed": 0.01,
    "max_energy": 5,
    "field_x": 10,
    "field_y": 10,
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
    theta_d = degrees(atan2(d_y, d_x)) - org.current_direction
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
        self.layers_number = 4
        self.neurons_number_in_layer = 3
        self.name = name
        self.intelegence = 2
        self.max_rot_speed = 15
        self.max_move_speed = 2
        self.neural_matrix = neural_matrix

        # features
        self.features_dict = full_features_dict
        self.features_list = []
        # decisions
        self.current_speed = 0
        self.current_rotation_speed = 0
        self.desired_direction = 0

        self.decisions_dict = decisions_dict
        self.neural_matrix = []
        if not neural_matrix:
            self.neural_matrix = []
            self.neural_matrix.append(np.random.uniform(-1, 1, (len(self.features_dict), self.neurons_number_in_layer)))
            for i in range(self.layers_number - 2):
                self.neural_matrix.append(
                    np.random.uniform(-1, 1, (self.neurons_number_in_layer, self.neurons_number_in_layer)))
            self.neural_matrix.append(
                np.random.uniform(-1, 1, (self.neurons_number_in_layer, len(decisions_dict))))

    # NEURAL NETWORK
    def think(self):

        # SIMPLE MLP
        if len(self.features_list) > 0:
            list_of_features = numpy.array(self.features_list).reshape(1,3)

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
        if self.current_rotation_speed > self.max_rot_speed:
            self.current_rotation_speed = self.max_rot_speed
        if self.current_rotation_speed < -self.max_rot_speed:
            self.current_rotation_speed = -self.max_rot_speed

        self.current_direction += self.current_rotation_speed
        self.current_direction = self.current_rotation_speed

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


class food_f():
    def __init__(self):
        self.x = uniform(0, settings['field_x'])
        self.y = uniform(0, settings['field_y'])
        self.energy = random.randint(1, settings["max_energy"])


def simulate(organisms, foods_list):
    # UPDATE FITNESS FUNCTION
    for food in foods_list:
        for org in organisms:
            food_org_dist = dist(org.x, org.y, food.x, food.y)

            # UPDATE FITNESS FUNCTION
            if food_org_dist <= 0.075:
                org.food_count += food.energy

    for org in organisms:
        org.food_count -= 0.1
        if food.energy <= 0:
            organisms.remove(org)

    for fd in foods_list:
        if fd.energy <= 0:
            foods.remove(fd)
            foods.append(food_f())

    # CALCULATE HEADING TO NEAREST FOOD SOURCE
    def number_of_org_around_food(f):
        cnt = 0
        for org in organisms:
            if dist(org.x, org.y, f.x, f.y) < 2:
                cnt += 1
        return cnt

    for food in foods_list:
        for org in organisms:

            # CALCULATE VECTORS
            food_org_dist = dist(org.x, org.y, food.x, food.y)
            org.features_list = []
            if food_org_dist < org.vision_range:
                org.features_list.append([food_org_dist, food.energy, number_of_org_around_food(food)])
    # GET ORGANISM RESPONSE
    for org in organisms:
        org.think()

    # UPDATE ORGANISMS POSITION AND VELOCITY
    for org in organisms:
        org.update_r()
        org.update_vel()
        org.update_pos()


def plot_frame(organisms, foods):
    plt.clf()
    # PLOT ORGANISMS
    fig, ax = plt.subplots()
    fig.set_size_inches(9.6, 5.4)
    for organism in organisms:
        circle = Circle([organism.x, organism.y], 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
        ax.add_artist(circle)

        edge = Circle([organism.x, organism.y], 0.05, facecolor='None', edgecolor='darkgreen', zorder=8)
        ax.add_artist(edge)

        tail_len = 0.075

        x2 = cos(radians(organism.current_direction)) * tail_len + organism.x
        y2 = sin(radians(organism.current_direction)) * tail_len + organism.y

        ax.add_line(lines.Line2D([organism.x, x2], [organism.y, y2], color='darkgreen', linewidth=1, zorder=10))

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


amebas = [organism(x) for x in range(1, 100)]
foods = [food_f() for x in range(1, 100)]

while True:
    simulate(amebas, foods)
    #plot_frame(amebas, foods)
    print(1)
    #sleep(1.0)
