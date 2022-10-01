from matplotlib import pyplot as plt
from matplotlib.patches import Circle

from utils import colors


def plot(ax_local, amebas, foods, step_count, gen_num, yx_local, folder):
    ax_local.clear()
    cnts = [0 for _ in range(gen_num)]
    for a_data in amebas:
        # pylint: disable=R0913
        # pylint: disable-msg=too-many-arguments
        edge = Circle([a_data.x, a_data.y], 0.01, facecolor='None', edgecolor='darkgreen', zorder=8)
        circle = Circle([a_data.x, a_data.y], 0.01, edgecolor='g', facecolor=colors[a_data.generation - 1], zorder=8,
                        alpha=0.4)

        ax_local.add_artist(edge)
        ax_local.add_artist(circle)
        ax_local.text(a_data.x - 0.005, a_data.y - 0.005, str(a_data.generation), fontsize=6)
        cnts[a_data.number // 10000] += 1
    for f_data in foods:
        circle = Circle([f_data.x, f_data.y], 0.005, edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
        ax_local.add_artist(circle)
    for i in range(len(yx_local)):
        yx_local[i].append(cnts[i])

    plt.savefig(f"{folder}/" + str(step_count).zfill(6) + '.png', dpi=100)
    return cnts
