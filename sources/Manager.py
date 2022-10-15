"""
Manager file
"""
# pylint: disable=too-many-instance-attributes
# pylint: disable=invalid-name
# Reasonable in this case
import json
import random

import cv2
import numpy as np
from matplotlib import pyplot as plt

from food import Food
from organims import Organism
from ploting import plot
from settings import settings_game_default
from utils import dist, create_folder


class GameManager:
    """
    GameManager is responsible for the game. Put settings and start
    """

    def __init__(self, sett=None, write_settings_to_file=False, local=None):

        if not sett:
            self.sett = settings_game_default
        else:
            self.sett = sett
        self.local = None

        self.current_image = None

        if local:
            self.local = local

        if write_settings_to_file:
            with open("setting.json", "w", encoding="utf-8") as outfile:
                json.dump(self.sett, outfile, indent=4)

        create_folder(self.sett["image_folder"])

        self.fig, self.ax_plot = plt.subplots()
        self.ax_plot.set_xlim([0, 2])
        self.fig.set_size_inches(9.6, 9.6)



        self.amebas = [Organism(x, self.sett,
                                tag=f"{x}") for x in range(1, self.sett["amebas_number"])]

        self.foods = [Food(self.sett) for _ in range(1, self.sett["food_number"])]

        self.gen_num = 100
        self.counts_of_generation = [[] for i in range(self.gen_num)]

        self.steps = self.sett["max_steps"]
        self.x_count = range(0, self.steps)
        self.step_count = 0
        self.images = []

    def start(self):
        """
        Start game. Creating plot of field on each step
        Executing until count of organizms more than 0 or count of steps is zero

        :return: true when ends and false if got some exception
        """
        self.images = []
        out = cv2.VideoWriter('project.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, (960, 960))
        try:
            while self.step_count < self.steps:
                if len(self.amebas) == 0:
                    x = random.randint(1, self.sett["amebas_number"])
                    self.amebas.append(Organism(x, self.sett, tag=f"{x}"))
                self.amebas.sort(key=lambda x: x.max_move_speed, reverse=True)

                self.simulate(self.amebas, self.foods)
                counts, img = plot(self.ax_plot, self.amebas, self.foods,
                                   self.gen_num, self.counts_of_generation,
                                   self.fig, self.sett)
                self.step_count += 1
                self.current_image = img
                out.write(img)
                if self.local:
                    self.images.append(img)

                data_str = "_".join(map(str, list(filter(lambda x: x > 0, counts))))
                data_str = f"{self.step_count}_{len(self.amebas)}_{len(self.foods)}:::{data_str}"
                print(data_str)

        except ValueError as exep:
            print(f'Failed. Reason: {exep}')
            return False

        out.release()

        if len(self.amebas) > 0:
            tag_counter = {}

            for am in self.amebas:
                if am.tag in tag_counter:
                    tag_counter[am.tag] += 1
                else:
                    tag_counter[am.tag] = 1
            print("Counting tags:")
            print(tag_counter)
            print("biggest amebas:")
            self.amebas.sort(key=lambda x: x.size, reverse=True)
            print(*(self.amebas[:5]), sep='\n')

            print("smartes amebas:")
            self.amebas.sort(key=lambda x: x.intelligence, reverse=True)
            print(*(self.amebas[:5]), sep='\n')

            meanSize = np.mean([c.size for c in self.amebas])
            print(f"Average size: {meanSize}")

            meanInt = np.mean([c.intelligence for c in self.amebas])
            print(f"Average int: {meanInt}")

            meanMaxSpeed = np.mean([c.max_move_speed for c in self.amebas])
            print(f"Average maxSpeed: {meanMaxSpeed}")

    def getCurrentImage(self):
        """
        :return: Return current image to videostream
        """
        return self.current_image

    def simulate(self, organisms, foods_list):
        """
        :param organisms: list of organizms
        :param foods_list: list of foods
        :return: nothing
        """
        for org in organisms:
            for food in foods_list:
                food_org_dist = dist(org, food)
                if food_org_dist <= (self.sett["feed_distance"] * org.size_coef()):
                    org.food_count += food.energy
                    foods_list.remove(food)
                    break

        for _ in range(0, self.sett["food_update"]):
            foods_list.append(Food(self.sett))

        # CALCULATE HEADING TO NEAREST FOOD SOURCE
        # pylint: disable=line-too-long
        def number_of_org_around_food(current_food):
            cnt_l = 0
            for org_l in organisms:
                if abs(org_l.position_x - current_food.position_x) < float(org_l.vision_range) / 2 and \
                        abs(org_l.position_y - current_food.position_y) < float(org_l.vision_range) / 2:
                    cnt_l += 1
            return cnt_l

        # calculate features for nn
        for food in foods_list:
            food_num = number_of_org_around_food(food)
            for org in organisms:
                food_org_dist = dist(org, food)
                org.features_list = []
                if food_org_dist < org.vision_range:
                    org.features_list.append([food_org_dist, food.energy, food_num])

        # GET ORGANISM RESPONSE
        for org in organisms:
            org.think()

        for org in organisms:
            org.update_energy(self.sett["step_energy_drain"])
            if org.food_count <= 0:
                organisms.remove(org)
        for org in organisms:
            if org.food_count >= (org.size * org.ready_for_sex):
                organisms.append(org.mutate(self.sett))
