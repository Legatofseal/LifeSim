"""
Plot current game state
"""
import cv2
import numpy as np
from matplotlib.patches import Circle

from utils import colors


# pylint: disable=too-many-arguments
# Reasonable in this case
def plot(ax_local, amebas, foods, gen_num, yx_local, fig):
    """
    Function that save current state as image
    :param ax_local: plot
    :param amebas: list of organizms to plot
    :param foods: list of organizms to plot
    :param step_count:
    :param gen_num:
    :param yx_local:
    :param folder:
    :return:
    """
    ax_local.clear()
    cnts = [0 for _ in range(gen_num)]
    for a_data in amebas:
        # pylint: disable=R0913
        # pylint: disable-msg=too-many-arguments
        edge = Circle([a_data.position_x, a_data.position_y], a_data.size / (50 * 100),
                      facecolor='None', edgecolor='darkgreen', zorder=8)
        circle = Circle([a_data.position_x, a_data.position_y], a_data.size / (50 * 100),
                        edgecolor='g', facecolor=colors[a_data.generation - 1], zorder=8,
                        alpha=0.4)

        ax_local.add_artist(edge)
        ax_local.add_artist(circle)
        ax_local.text(a_data.position_x - 0.005, a_data.position_y - 0.005,
                      str(a_data.generation), fontsize=6)
        cnts[a_data.number // 10000] += 1
    for f_data in foods:
        circle = Circle([f_data.position_x, f_data.position_y], 0.005,
                        edgecolor='darkslateblue', facecolor='mediumslateblue', zorder=5)
        ax_local.add_artist(circle)
    for i in range(len(yx_local)):
        yx_local[i].append(cnts[i])

    fig.canvas.draw()

    img = cv2.cvtColor(np.asarray(fig.canvas.buffer_rgba()), cv2.COLOR_RGBA2BGR)
    img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return cnts, img
