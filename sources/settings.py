from collections import OrderedDict

settings = {
    "default_size": 50,
    "default_speed": 0.01,
    "max_energy": 10,
    "field_x": 1,
    "field_y": 1,
    "max_speed": 2,
    "feed_distance": 0.035,
    "amebas_number": 6,
    "food_number": 50,
    "max_steps": 1200,
    "step_energy_drain": 0.5,
    "food_update": 10,
    "mut_factor": 10,

}
full_features_dict = OrderedDict([("food_distance", 0), ("food_size", 0), ("org_around_food", 0)])
decisions_dict = OrderedDict([("current_speed", 0), ("current_rotation_speed", 0), ("desired_direction", 0)])
