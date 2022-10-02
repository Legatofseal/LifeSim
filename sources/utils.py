"""
utils for game
"""
# pylint: disable=maybe-no-member
import glob
from math import degrees, atan2
import random
import cv2

colors = [
    "lightgreen",
    "rosybrown",
    "lavender",
    "plum",
    "magenta",
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
    return (random.random(), random.random(), random.random())


for i in range(0, 150):
    colors.append(random_color())


def create_video(folder, list_images=None):
    """
    Create video from after game, from folder or list of images
    :param folder: folder
    :param list_images: list_images
    :return: nothing
    """
    # Function to plot
    if not list_images:
        img_array = []
        for filename in glob.glob(f'{folder}/*.png'):
            img = cv2.imread(filename)
            height, width, _ = img.shape
            size = (width, height)
            img_array.append(img)
    else:
        size = list_images[0].size
        img_array = list_images
    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for _ in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def dist(x_first, y_first, x_second, y_second):
    """
    calculate distanse between two entities
    :param x_first: x_first
    :param y_first: y_first
    :param x_second: x_second
    :param y_second: y_second
    :return: distance
    """
    return ((x_second - x_first) ** 2 + (y_second - y_first) ** 2) ** 0.5


def calc_heading(org, food):
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
