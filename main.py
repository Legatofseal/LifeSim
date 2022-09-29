from __future__ import division, print_function

from time import sleep, time

import numpy
import numpy as np

from math import cos, sqrt, degrees, atan2
from math import radians
from math import sin
from random import uniform
from collections import OrderedDict
import random
from time import sleep
from matplotlib.patches import Circle

from plotting import plot_food
from plotting import plot_organism

from matplotlib import pyplot as plt, lines
from collections import Counter

settings = {
    "default_size": 120,
    "default_speed": 0.01,
    "max_energy": 5,
    "field_x": 2,
    "field_y": 2,
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

        self.mut_factor = 10
        self.neural_matrix = []
        if not neural_matrix:
            self.neural_matrix = []
            self.neural_matrix.append(np.random.uniform(-1, 1, (len(self.features_dict), self.neurons_number_in_layer)))
            for i in range(self.layers_number - 2):
                self.neural_matrix.append(
                    np.random.uniform(-1, 1, (self.neurons_number_in_layer, self.neurons_number_in_layer)))
            self.neural_matrix.append(
                np.random.uniform(-1, 1, (self.neurons_number_in_layer, len(decisions_dict))))
        else:
            self.neural_matrix = neural_matrix

    def mutate(self):

        n_neural = []
        for m in self.neural_matrix:
            n_neural.append(m * (1 + uniform(-self.mut_factor, self.mut_factor)))
        n = organism(10000 + self.number, n_neural)
        n.food_count = self.size / 2  # fitness (food count)
        return n

    # NEURAL NETWORK
    def think(self):

        # SIMPLE MLP
        if len(self.features_list) > 0:
            list_of_features = numpy.array(self.features_list).reshape(1, 3)

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

    for org in organisms:
        for food in foods_list:
            food_org_dist = dist(org.x, org.y, food.x, food.y)

            # UPDATE FITNESS FUNCTION
            if food_org_dist <= 0.075:
                org.food_count += food.energy
                foods_list.remove(food)
                break

    for org in organisms:
        org.food_count -= 2
        if org.food_count <= 0:
            organisms.remove(org)
        if org.food_count >= (org.size * 3 / 4):
            organisms.append(org.mutate())

    for fd in range(0, 15):
        foods_list.append(food_f())

    # CALCULATE HEADING TO NEAREST FOOD SOURCE
    def number_of_org_around_food(f):
        cnt_l = 0
        for org_l in organisms:
            if dist(org_l.x, org_l.y, f.x, f.y) < 2:
                cnt_l += 1
        return cnt_l

    for food in foods_list:
        for org in organisms:
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


amebas = [organism(x) for x in range(1, 50)]
foods = [food_f() for x in range(1, 1200)]
'''
x = [10]
y = [10]

plt.ion()

figure, ax = plt.subplots(figsize=(8, 8))
line1, = ax.plot(x, y)

plt.title("Dynamic Plot of sinx", fontsize=25)

plt.xlabel("X", fontsize=18)
plt.ylabel("sinX", fontsize=18)
circle = Circle([1, 1], 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
'''
cnt = 0
yx = [[] for i in range(10)]
cnts = [0 for i in range(10)]

steps = 1000
x = [a for a in range(0, steps)]
step_count = 0
while len(amebas) > 0 and step_count < steps:
    cnts = [0 for i in range(10)]
    random.shuffle(amebas)
    simulate(amebas, foods)
    step_count += 1

    '''
   
    circle = Circle([50, 50], 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
    for o in amebas:
        circle = Circle([o.x, o.y], 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
        ax.add_artist(circle)

        edge = Circle([o.x, o.y], 0.05, facecolor='None', edgecolor='darkgreen', zorder=8)
        ax.add_artist(edge)


    figure.canvas.draw()

    figure.canvas.flush_events()
    '''
    # plot_frame(amebas, foods)
    for a in amebas:
        cnts[a.number // 10000] += 1
    for i in range(len(yx)):
        yx[i].append(cnts[i])

    sleep(0.1)

    data_str = "_".join(map(str, cnts))
    data_str = f"{step_count}_{len(amebas)}_{len(foods)}:::{data_str}"
    print(data_str)

# Function to plot
plt.figure(figsize=(10, 10))
for i in range(len(yx)):
    if max(yx[i]) > 0:
        plt.plot(x[0:len(yx[i])], yx[i], label=f"gen{i + 1}")

# Function add a legend
# plt.legend(["gen1", "gen2","gen3", "gen4", "gen5", "gen6", "gen7", "gen8", "gen9", "gen10"], loc="lower right")
plt.legend()
plt.title(f"Amebas Generations for {steps} steps")
# function to show the plot
plt.show()
