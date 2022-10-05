# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=line-too-long, too-many-instance-attributes
import os.path
from os import walk
import numpy as np
import pytest
from PIL import Image
from sources.food import Food
from sources.organims import Organism
from sources.settings import settings_game_default
from sources.utils import random_color, create_folder, create_video, dist, calc_heading


class TestUtils:
    @pytest.fixture
    def get_settings(self):
        return settings_game_default

    def test_random_color(self):
        color = random_color()
        assert isinstance(color, tuple)
        assert len(color) == 3

    def test_create_video(self, tmp_path):
        folder = "test"
        fld = tmp_path / folder
        create_folder(fld)

        width, height = 100, 100
        for i in range(10):
            random_array = np.random.randint(low=0, high=255, size=(width, height), dtype=np.uint8)
            random_im = Image.fromarray(random_array)
            random_im.save(fld / f"img_{i}.png")
        create_video(fld)
        assert os.path.isfile("project.avi")

    def test_create_folder(self, tmp_path):
        folder = "test"
        fld = tmp_path / folder
        create_folder(fld)

        assert os.path.isdir(fld)

        file_name = fld / "test.txt"

        with open(file_name, "w", encoding="utf-8", ) as file:
            file.write("test")

        create_folder(folder)
        file_list = []
        for (_, _, filenames) in walk(folder):
            file_list.extend(filenames)

        assert len(file_list) == 0

    @pytest.mark.parametrize("coords, distance",
                             [([1, 1, 1, 1], 0),
                              ([0, 0, 1, 1], 2**0.5),
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
