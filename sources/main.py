"""
Main file
"""
# pylint: disable=import-error
from __future__ import division, print_function

import json
import argparse

from sources.Manager import GameManager


def main():
    """
    Create Manager instance and start the game
    :return: nothing
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--settings", help="json file with settings")
    args = parser.parse_args()

    manager = None

    if args.settings:
        try:
            with open(args.settings, "r", encoding="utf-8") as file_sett:
                manager = GameManager(json.load(file_sett))

        except FileNotFoundError as error:
            print(f"Can not open settings file : {error}. Loading default settings")

        except json.decoder.JSONDecodeError as error:
            print(f"Cannot convert json to dict : {error}. Loading default settings")

    if not manager:
        manager = GameManager()

    manager.start()
    manager.create_video_after_game()


if __name__ == "__main__":
    main()
