"""
Main file
"""
# pylint: disable=import-error
from __future__ import division, print_function

import json
import os
import shutil
from matplotlib import pyplot as plt
from food import Food
from organims import Organism
from settings import settings_game_default
from utils import create_video, dist
from sources.ploting import plot


# pylint: disable=too-many-instance-attributes
# Reasonable in this case
class GameManager:
    """
    GameManager is responsible for the game. Put settings and start
    """
    def __init__(self, sett=None, write_settings_to_file=False):

        if not sett:
            self.sett = settings_game_default
        else:
            self.sett = sett

        if write_settings_to_file:
            json_object = json.dumps(self.sett, indent=4)
            with open("setting.json", "w", encoding="utf-8") as outfile:
                json.dump(json_object, outfile)

        if not os.path.exists(self.sett["image_folder"]):
            os.makedirs(self.sett["image_folder"])

        for filename in os.listdir(self.sett["image_folder"]):
            file_path = os.path.join(self.sett["image_folder"], filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except FileNotFoundError as exep:
                print(f'Failed to delete {file_path}. Reason: {exep}')

        self.fig, self.ax_plot = plt.subplots()
        self.fig.set_size_inches(9.6, 9.6)

        plt.xlim(0, self.sett["field_x"])
        plt.ylim(0, self.sett["field_y"])

        self.amebas = [Organism(x, self.sett) for x in range(1, self.sett["amebas_number"])]
        self.foods = [Food(self.sett) for _ in range(1, self.sett["food_number"])]

        self.gen_num = 100
        self.counts_of_generation = [[] for i in range(self.gen_num)]

        self.steps = self.sett["max_steps"]
        self.x_count = range(0, self.steps)
        self.step_count = 0

    def start(self):
        """
        Start game. Creating plot of field on each step
        Executing until count of organizms more than 0 or count of steps is zero

        :return: true when ends and false if got some exception
        """
        try:
            while len(self.amebas) > 0 and self.step_count < self.steps:
                self.simulate(self.amebas, self.foods)
                counts = plot(self.ax_plot, self.amebas, self.foods, self.step_count,
                              self.gen_num, self.counts_of_generation,
                              self.sett["image_folder"])
                self.step_count += 1

                data_str = "_".join(map(str, list(filter(lambda x: x > 0, counts))))
                data_str = f"{self.step_count}_{len(self.amebas)}_{len(self.foods)}:::{data_str}"
                print(data_str)
        except ValueError as exep:
            print(f'Failed. Reason: {exep}')
            return False

    def create_video_after_game(self):
        """
        create video from set of images after games end
        :return: nothing
        """
        create_video(self.sett["image_folder"])

    def simulate(self, organisms, foods_list):
        """
        :param organisms: list of organizms
        :param foods_list: list of foods
        :return: nothing
        """
        for org in organisms:
            for food in foods_list:
                food_org_dist = dist(org.position_x, org.position_y,
                                     food.position_x, food.position_y)

                if food_org_dist <= self.sett["feed_distance"]:
                    org.food_count += food.energy
                    foods_list.remove(food)
                    break

        for org in organisms:
            org.food_count -= self.sett["step_energy_drain"]
            if org.food_count <= 0:
                organisms.remove(org)
            if org.food_count >= (org.size * org.ready_for_sex):
                organisms.append(org.mutate(self.sett))

        # pylint: disable=unused-argument
        for _ in range(0, self.sett["food_update"]):
            foods_list.append(Food(self.sett))

        # CALCULATE HEADING TO NEAREST FOOD SOURCE
        def number_of_org_around_food(current_food):
            cnt_l = 0
            for org_l in organisms:
                if abs(org_l.position_x - current_food.position_x) < 0.5 and \
                        abs(org_l.position_y - current_food.position_y) < 0.5:
                    cnt_l += 1
            return cnt_l

        for food in foods_list:
            food_num = number_of_org_around_food(food)
            for org in organisms:
                food_org_dist = dist(org.position_x, org.position_y,
                                     food.position_x, food.position_y)
                org.features_list = []
                if food_org_dist < org.vision_range:
                    org.features_list.append([food_org_dist, food.energy, food_num])

        # GET ORGANISM RESPONSE
        for org in organisms:
            org.think()


def main():
    """
    Create Manager instanse and start the game
    :return: nothing
    """
    manager = GameManager()
    manager.start()
    manager.create_video_after_game()


if __name__ == "__main__":
    main()