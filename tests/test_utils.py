# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long, too-many-instance-attributes

import pytest
from sources.food import Food
from sources.organims import Organism
from sources.settings import settings_game_default
from sources.utils import random_color, dist, calc_heading


class TestUtils:
    @pytest.fixture
    def get_settings(self):
        return settings_game_default

    def test_random_color(self):
        color = random_color()
        assert isinstance(color, tuple)
        assert len(color) == 3

    @pytest.mark.parametrize("coords, distance",
                             [([1, 1, 1, 1], 0),
                              ([0, 0, 1, 1], 2 ** 0.5),
                              ([0, 1, 1, 1], 1)])
    def test_dist(self, get_settings, coords, distance):
        org = Organism(1, get_settings)
        org.position_x = coords[0]
        org.position_y = coords[1]
        food = Food(get_settings)
        food.position_x = coords[2]
        food.position_y = coords[3]
        assert dist(org, food) == distance

    def test_calc_heading(self, get_settings):
        org = Organism(1, get_settings)
        org.position_x = 0
        org.position_y = 0
        food = Food(get_settings)
        food.position_x = 1
        food.position_y = 1
        assert calc_heading(org, food) == 0.25
