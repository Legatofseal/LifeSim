import glob
from cmath import sqrt
from math import degrees, atan2

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


def create_video(folder):
    # Function to plot
    img_array = []
    for filename in glob.glob(f'{folder}/*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def dist(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calc_heading(org, food):
    d_x = food.x - org.x
    d_y = food.y - org.y
    theta_d = degrees(atan2(d_y, d_x)) - org.current_direction
    if abs(theta_d) > 180: theta_d += 360
    return theta_d / 180
