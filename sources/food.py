"""
This module define food class
"""
# pylint: disable=missing-class-docstring
# pylint: disable=too-few-public-methods
from random import uniform
import random

from sources.entity import Entity


class Food(Entity):
    def __init__(self, sett):
        """
         :param sett: game settings
         """
        super().__init__()
        self.position_x = uniform(0, sett['field_x'])
        self.position_y = uniform(0, sett['field_y'])
        self.energy = random.randint(1, sett["max_energy"])

    def set_energy(self, val):
        """
        :param val: energy to set
        :return: nothing
        """
        self.energy = val
