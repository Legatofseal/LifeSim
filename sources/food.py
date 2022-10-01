from random import uniform
import random
from settings import settings_game


class food_f:
    def __init__(self):
        self.x = uniform(0, settings_game['field_x'])
        self.y = uniform(0, settings_game['field_y'])
        self.energy = random.randint(1, settings_game["max_energy"])
