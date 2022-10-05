"""
utils for game
"""
# pylint: disable=maybe-no-member
import glob
import os
import shutil
from math import degrees, atan2
import random
import cv2

from sources.Entity import Entity

NUM_OF_COLORS = 150

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
    return random.random(), random.random(), random.random()


for i in range(0, NUM_OF_COLORS):
    colors.append(random_color())


def create_folder(folder):
    """
    Create folder or clear if exist
    :param folder:
    :return:
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except FileNotFoundError as exep:
            print(f'Failed to delete {file_path}. Reason: {exep}')


def create_video(folder, list_images=None):
    """
    Create video from after game, from folder or list of images
    :param folder: folder
    :param list_images: list_images
    :return: nothing
    """
    # Function to plot
    img_array = []
    if not list_images:
        for filename in glob.glob(f'{folder}/*.png'):
            img = cv2.imread(filename)
            height, width, _ = img.shape
            size = (width, height)
            img_array.append(img)
    else:
        size = list_images[0].size
        img_array = list_images
    out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

    for img in img_array:
        out.write(img)
    out.release()


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
