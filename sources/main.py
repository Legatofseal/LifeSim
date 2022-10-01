from __future__ import division, print_function
from math import cos
from math import radians
from math import sin

from time import sleep
from matplotlib.patches import Circle

from matplotlib import pyplot as plt

from food import food_f
from organims import organism
from settings import settings
from utils import colors, create_video, dist




def simulate(organisms, foods_list):
    # UPDATE FITNESS FUNCTION

    for org in organisms:
        for food in foods_list:
            food_org_dist = dist(org.x, org.y, food.x, food.y)

            # UPDATE FITNESS FUNCTION
            if food_org_dist <= settings["feed_distance"]:
                org.food_count += food.energy
                foods_list.remove(food)
                break

    for org in organisms:
        org.food_count -= settings["step_energy_drain"]
        if org.food_count <= 0:
            organisms.remove(org)
        if org.food_count >= (org.size * 3 / 4):
            organisms.append(org.mutate())

    for fd in range(0, settings["food_update"]):
        foods_list.append(food_f())

    # CALCULATE HEADING TO NEAREST FOOD SOURCE
    def number_of_org_around_food(f):
        cnt_l = 0
        for org_l in organisms:
            if dist(org_l.x, org_l.y, f.x, f.y) < 2:
                cnt_l += 1
        return cnt_l

    for food in foods_list:
        for org in organisms:
            food_org_dist = dist(org.x, org.y, food.x, food.y)
            org.features_list = []
            if food_org_dist < org.vision_range:
                org.features_list.append([food_org_dist, food.energy, number_of_org_around_food(food)])

    # GET ORGANISM RESPONSE
    for org in organisms:
        org.think()

    # UPDATE ORGANISMS POSITION AND VELOCITY
    for org in organisms:
        org.update_r()
        org.update_vel()
        org.update_pos()



fig, ax = plt.subplots()
fig.set_size_inches(9.6, 9.6)

plt.xlim(0, settings["field_x"])
plt.ylim(0, settings["field_y"])

amebas = [organism(x) for x in range(1, settings["amebas_number"])]
foods = [food_f() for x in range(1, settings["food_number"])]

'''
x = [10]
y = [10]

plt.ion()

figure, ax = plt.subplots(figsize=(8, 8))
line1, = ax.plot(x, y)

plt.title("Dynamic Plot of sinx", fontsize=25)

plt.xlabel("X", fontsize=18)
plt.ylabel("sinX", fontsize=18)
circle = Circle([1, 1], 0.05, edgecolor='g', facecolor='lightgreen', zorder=8)
'''
cnt = 0
yx = [[] for i in range(15)]
cnts = [0 for i in range(15)]

steps = settings["max_steps"]
x = [a for a in range(0, steps)]
step_count = 0


while len(amebas) > 0 and step_count < steps:
    cnts = [0 for i in range(15)]
    simulate(amebas, foods)
    step_count += 1
    ax.clear()
    for a in amebas:
        #print(f"{a.x}_{a.y}")
        edge = Circle([a.x, a.y], 0.01, facecolor='None', edgecolor='darkgreen', zorder=8)
        circle = Circle([a.x, a.y], 0.01, edgecolor='g', facecolor=colors[a.generation - 1], zorder=8, alpha=0.4)
        tail_len = 0.013

        rx = cos(radians(a.current_direction))
        ry = sin(radians(a.current_direction))

        x2 = rx * tail_len + a.x
        y2 = ry * tail_len + a.y

        #ax.add_line(lines.Line2D([a.x, x2], [a.y, y2], color='darkgreen', linewidth=1, zorder=10))
        ax.add_artist(edge)
        ax.add_artist(circle)
        ax.text(a.x - 0.005, a.y - 0.005, str(a.generation), fontsize=6)
        cnts[a.number // 10000] += 1
    for f in foods:
        circle = Circle([f.x, f.y], 0.005, edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
        ax.add_artist(circle)
    for i in range(len(yx)):
        yx[i].append(cnts[i])
    plt.savefig("images/" + str(step_count).zfill(4) + '.png', dpi=100)
    sleep(0.1)

    data_str = "_".join(map(str, cnts))
    data_str = f"{step_count}_{len(amebas)}_{len(foods)}:::{data_str}"
    print(data_str)

create_video("images")

plt.figure(figsize=(10, 10))
for i in range(len(yx)):
    if max(yx[i]) > 0:
        plt.plot(x[0:len(yx[i])], yx[i], label=f"gen{i + 1}")

# Function add a legend
# plt.legend(["gen1", "gen2","gen3", "gen4", "gen5", "gen6", "gen7", "gen8", "gen9", "gen10"], loc="lower right")
plt.legend()
plt.title(f"Amebas Generations for {steps} steps")
# function to show the plot
plt.show()
