import glob
from math import degrees, atan2
import random

import cv2
import numpy as np

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
    return (random.random(), random.random(), random.random())


for i in range(0, 150):
    colors.append(random_color())


def create_video(folder, list_images=None):
    # Function to plot
    if not list_images:
        img_array = []
        for filename in glob.glob(f'{folder}/*.png'):
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)
            img_array.append(img)
    else:
        size = list_images[0].size
        img_array = list_images
    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


def dist(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def calc_heading(org, food):
    d_x = food.x - org.x
    d_y = food.y - org.y
    theta_d = degrees(atan2(d_y, d_x)) - org.current_direction
    if abs(theta_d) > 180: theta_d += 360
    return theta_d / 180
