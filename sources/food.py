from random import uniform, random

from settings import settings


class food_f():
    def __init__(self):
        self.x = uniform(0, settings['field_x'])
        self.y = uniform(0, settings['field_y'])
        self.energy = random.randint(1, settings["max_energy"])
