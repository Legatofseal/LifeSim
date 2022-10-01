from __future__ import division, print_function
import os
import shutil
from matplotlib import pyplot as plt
from food import food_f
from organims import organism
from settings import settings_game
from utils import create_video, dist
from sources.ploting import plot


class GameManager:
    def __init__(self, sett=None):
        if not os.path.exists(settings_game["image_folder"]):
            os.makedirs(settings_game["image_folder"])
        for filename in os.listdir(settings_game["image_folder"]):
            file_path = os.path.join(settings_game["image_folder"], filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as exep:
                print('Failed to delete %s. Reason: %s' % (file_path, exep))
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(9.6, 9.6)

        plt.xlim(0, settings_game["field_x"])
        plt.ylim(0, settings_game["field_y"])

        self.amebas = [organism(x) for x in range(1, settings_game["amebas_number"])]
        self.foods = [food_f() for _ in range(1, settings_game["food_number"])]

        self.gen_num = 100
        self.yx = [[] for i in range(self.gen_num)]

        self.steps = settings_game["max_steps"]
        self.x = [a for a in range(0, self.steps)]
        self.step_count = 0

    def start(self):
        while len(self.amebas) > 0 and self.step_count < self.steps:
            self.simulate(self.amebas, self.foods)
            counts = plot(self.ax, self.amebas, self.foods, self.step_count, self.gen_num, self.yx,
                        settings_game["image_folder"])
            self.step_count += 1

            data_str = "_".join(map(str, list(filter(lambda x: x > 0, counts))))
            data_str = f"{self.step_count}_{len(self.amebas)}_{len(self.foods)}:::{data_str}"
            print(data_str)

        create_video(settings_game["image_folder"])

    def simulate(self, organisms, foods_list):

        for org in organisms:
            for food in foods_list:
                food_org_dist = dist(org.x, org.y, food.x, food.y)

                if food_org_dist <= settings_game["feed_distance"]:
                    org.food_count += food.energy
                    foods_list.remove(food)
                    break

        for org in organisms:
            org.food_count -= settings_game["step_energy_drain"]
            if org.food_count <= 0:
                organisms.remove(org)
            if org.food_count >= (org.size * org.ready_for_sex):
                organisms.append(org.mutate())

        for fd in range(0, settings_game["food_update"]):
            foods_list.append(food_f())

        # CALCULATE HEADING TO NEAREST FOOD SOURCE
        def number_of_org_around_food(f):
            cnt_l = 0
            for org_l in organisms:
                if abs(org_l.x - f.x) < 0.5 and abs(org_l.y - f.y) < 0.5:
                    cnt_l += 1
            return cnt_l

        for food in foods_list:
            food_num = number_of_org_around_food(food)
            for org in organisms:
                food_org_dist = dist(org.x, org.y, food.x, food.y)
                org.features_list = []
                if food_org_dist < org.vision_range:
                    org.features_list.append([food_org_dist, food.energy, food_num])

        # GET ORGANISM RESPONSE
        for org in organisms:
            org.think()


def main():
    GameManager().start()


if __name__ == "__main__":
    main()
