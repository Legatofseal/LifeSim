"""
Generate game statistic
"""
from collections import defaultdict
import statistics

from sources import Manager


def get_game_stat(manager:Manager):
    """
    Get field statistic
    """
    result = ""
    groups = defaultdict(list)

    for obj in manager.amebas:
        groups[obj.tag].append(obj)

    new_list = groups.values()
    result+=f"Step: {manager.step_count}\n"
    for team in new_list:
        result += f"{team[0].tag}: Number of organisms:{len(team)}, Total size: {round(sum(c.size for c in team),0)}," \
                  f" Avg speed: {round(statistics.mean(c.max_move_speed for c in team),3)}, Max Gen: {max(c.generation for c in team)}\n"
    result += f"Number of foods on field: {len(manager.foods)}\n"

    return result
