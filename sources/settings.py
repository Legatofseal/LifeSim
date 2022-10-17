"""
Settings for the game
"""
from collections import OrderedDict

settings_game_default = {
    "field_x": 1.5,
    "field_y": 1.5,
    "amebas_number": 6,
    "food_number": 50,
    "max_steps": 50,
    "food_update": 1,
    "max_energy": 10,
    "am_config": [
        {
            "tag": "Team1",
            "default_size": 50.0,
            "max_speed": 0.03,
            "step_energy_drain": 0.2,
            "mut_factor": 15,
            "feed_distance": 0.02,
        },
        {
            "tag": "Team2",
            "default_size": 50.0,
            "max_speed": 0.03,
            "step_energy_drain": 0.2,
            "mut_factor": 15,
            "feed_distance": 0.02,
        },
        {
            "tag": "Team3",
            "default_size": 50.0,
            "max_speed": 0.03,
            "step_energy_drain": 0.2,
            "mut_factor": 15,
            "feed_distance": 0.02,
        },
        {
            "tag": "Team4",
            "default_size": 50.0,
            "max_speed": 0.03,
            "step_energy_drain": 0.2,
            "mut_factor": 15,
            "feed_distance": 0.02,
        },
        {
            "tag": "Team5",
            "default_size": 50.0,
            "max_speed": 0.03,
            "step_energy_drain": 0.2,
            "mut_factor": 15,
            "feed_distance": 0.02,
        },
    ],
}


full_features_dict = OrderedDict([("food_distance", 0),
                                  ("food_size", 0), ("org_around_food", 0)])
decisions_dict = OrderedDict([("current_speed", 0), ("current_rotation_speed", 0),
                              ("desired_direction", 0)])
