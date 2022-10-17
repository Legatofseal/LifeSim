"""
utils for game
"""
# pylint: disable=maybe-no-member
from math import degrees, atan2
import random
from sources.entity import Entity

NUM_OF_COLORS = 150

colors_list = [
    "green",
    "magenta",
    "lavender",
    "plum",
    "red",
    "skyblue",
    "chocolate",
    "coral",
    "aquamarine",
    "azure",
    "gray",
    "darkred",
]


def random_color():
    """
    generate random color
    :return:
    """
    return random.random(), random.random(), random.random()

def dist(ent1: Entity, ent2: Entity):
    """
   :param ent1: first entity, food, organism etc
   :param ent2: second entity, food, organism etc
   :return: distance
   """
    return ((ent2.position_x - ent1.position_x) ** 2 +
            (ent2.position_y - ent1.position_y) ** 2) ** 0.5


def calc_heading(org:Entity, food:Entity):
    """
    Calculate heading to food
    :param org: organism
    :param food: food
    :return: heading in degrees
    """
    d_x = food.position_x - org.position_x
    d_y = food.position_y - org.position_y
    theta_d = degrees(atan2(d_y, d_x)) - org.current_direction
    if abs(theta_d) > 180:
        theta_d += 360
    return theta_d / 180
